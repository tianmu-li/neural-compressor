#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The utility of common module."""

import collections
import importlib
import subprocess
import time
from typing import Dict

import cpuinfo
import psutil
from prettytable import PrettyTable

from neural_compressor.common.utils import Mode, TuningLogger, logger

__all__ = [
    "set_workspace",
    "get_workspace",
    "set_random_seed",
    "set_resume_from",
    "set_tensorboard",
    "dump_elapsed_time",
    "log_process",
    "singleton",
    "LazyImport",
    "CpuInfo",
    "default_tuning_logger",
    "call_counter",
    "Statistics",
]


def singleton(cls):
    """Singleton decorator."""
    instances = {}

    def _singleton(*args, **kw):
        """Create a singleton object."""
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class LazyImport(object):
    """Lazy import python module till use."""

    def __init__(self, module_name):
        """Init LazyImport object.

        Args:
           module_name (string): The name of module imported later
        """
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        """Get the attributes of the module by name."""
        try:
            self.module = importlib.import_module(self.module_name)
            mod = getattr(self.module, name)
        except:
            spec = importlib.util.find_spec(str(self.module_name + "." + name))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        return mod

    def __call__(self, *args, **kwargs):
        """Call the function in that module."""
        function_name = self.module_name.split(".")[-1]
        module_name = self.module_name.split(f".{function_name}")[0]
        self.module = importlib.import_module(module_name)
        function = getattr(self.module, function_name)
        return function(*args, **kwargs)


@singleton
class CpuInfo(object):
    """CPU info collection."""

    def __init__(self):
        """Get whether the cpu numerical format is bf16, the number of sockets, cores and cores per socket."""
        self._bf16 = False
        self._vnni = False
        info = cpuinfo.get_cpu_info()
        if "arch" in info and "X86" in info["arch"]:
            cpuid = cpuinfo.CPUID()
            max_extension_support = cpuid.get_max_extension_support()
            if max_extension_support >= 7:
                ecx = cpuid._run_asm(
                    b"\x31\xC9",  # xor ecx, ecx
                    b"\xB8\x07\x00\x00\x00" b"\x0f\xa2" b"\x89\xC8" b"\xC3",  # mov eax, 7  # cpuid  # mov ax, cx  # ret
                )
                self._vnni = bool(ecx & (1 << 11))
                eax = cpuid._run_asm(
                    b"\xB9\x01\x00\x00\x00",  # mov ecx, 1
                    b"\xB8\x07\x00\x00\x00" b"\x0f\xa2" b"\xC3",  # mov eax, 7  # cpuid  # ret
                )
                self._bf16 = bool(eax & (1 << 5))

    @property
    def bf16(self):
        """Get whether it is bf16."""
        return self._bf16

    @property
    def vnni(self):
        """Get whether it is vnni."""
        return self._vnni


def dump_elapsed_time(customized_msg=""):
    """Get the elapsed time for decorated functions.

    Args:
        customized_msg (string, optional): The parameter passed to decorator. Defaults to None.
    """

    def f(func):
        def fi(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            logger.info(
                "%s elapsed time: %s ms"
                % (customized_msg if customized_msg else func.__qualname__, round((end - start) * 1000, 2))
            )
            return res

        return fi

    return f


def set_random_seed(seed: int):
    """Set the random seed in config."""
    from neural_compressor.common import options

    options.random_seed = seed


def set_workspace(workspace: str):
    """Set the workspace in config."""
    from neural_compressor.common import options

    options.workspace = workspace


def get_workspace():
    """Get the workspace in config."""
    from neural_compressor.common import options

    return options.workspace


def set_resume_from(resume_from: str):
    """Set the resume_from in config."""
    from neural_compressor.common import options

    options.resume_from = resume_from


def set_tensorboard(tensorboard: bool):
    """Set the tensorboard in config."""
    from neural_compressor.common import options

    options.tensorboard = tensorboard


default_tuning_logger = TuningLogger()


def log_process(mode=Mode.QUANTIZE):
    """Decorator function that logs the stage of process.

    Args:
        mode (Mode): The mode of the process.

    Returns:
        The decorated function.
    """

    def log_process_wrapper(func):
        def inner_wrapper(*args, **kwargs):
            start_log = default_tuning_logger.execution_start
            end_log = default_tuning_logger.execution_end

            start_log(mode=mode, stacklevel=4)

            # Call the original function
            result = func(*args, **kwargs)

            end_log(mode=mode, stacklevel=4)

            return result

        return inner_wrapper

    return log_process_wrapper


# decorator for recording number of times a function is called
FUNC_CALL_COUNTS: Dict[str, int] = collections.defaultdict(int)


def call_counter(func):
    """A decorator that keeps track of the number of times a function is called.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    def wrapper(*args, **kwargs):
        FUNC_CALL_COUNTS[func.__name__] += 1
        return func(*args, **kwargs)

    return wrapper


class Statistics:
    """The statistics printer."""

    def __init__(self, data, header, field_names, output_handle=logger.info):
        """Init a Statistics object.

        Args:
            data: The statistics data
            header: The table header
            field_names: The field names
            output_handle: The output logging method
        """
        self.field_names = field_names
        self.header = header
        self.data = data
        self.output_handle = output_handle
        self.tb = PrettyTable(min_table_width=40)

    def print_stat(self):
        """Print the statistics."""
        valid_field_names = []
        for index, value in enumerate(self.field_names):
            if index < 2:
                valid_field_names.append(value)
                continue

            if any(i[index] for i in self.data):
                valid_field_names.append(value)
        self.tb.field_names = valid_field_names
        for i in self.data:
            tmp_data = []
            for index, value in enumerate(i):
                if self.field_names[index] in valid_field_names:
                    tmp_data.append(value)
            if any(tmp_data[1:]):
                self.tb.add_row(tmp_data)
        lines = self.tb.get_string().split("\n")
        self.output_handle("|" + self.header.center(len(lines[0]) - 2, "*") + "|")
        for i in lines:
            self.output_handle(i)
