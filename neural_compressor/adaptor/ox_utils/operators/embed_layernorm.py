#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import onnx
from neural_compressor.adaptor.ox_utils.operators.ops import op_registry, Operator
from neural_compressor.adaptor.ox_utils.util import attribute_to_kwarg, ms_domain

@op_registry(op_types="EmbedLayerNormalization")
class EmbedLayerNormalizationOperator(Operator):
    def __init__(self, onnx_quantizer, onnx_node):
        super(EmbedLayerNormalizationOperator, self).__init__(onnx_quantizer, onnx_node)

    def quantize(self):
        node = self.node
        self.quantizer.quantize_inputs(node, [2, 3, 4, 5, 6])
        node.name = node.name + "_quant"

    def convert_check(self, convert_format):
        node = self.node
        assert convert_format in ['dynamic', 'static'], \
            "convert format for {} should be in ['dynamic', 'static']".format(node.op_type)
            
        if not node.name.endswith('_quant'):
            return False
        return True

    def convert(self, convert_format):
        node = self.node

        parents = [i for i in self.quantizer.model.get_parents(node) \
            if i.op_type == 'DequantizeLinear']
        inputs = []
        # 'input_ids'
        inputs.extend([node.input[0]])
        # 'segment_ids'
        inputs.extend([node.input[1]])
        for parent in parents:
            inputs.append(parent.input[0])
        # 'mask' (optional)
        if len(node.input) > 7:
            inputs.append(node.input[7])

        for parent in parents:
            inputs.append(parent.input[1])
        for parent in parents:
            inputs.append(parent.input[2])
 
        kwargs = {}
        for attribute in node.attribute: # pragma: no cover
            kwargs.update(attribute_to_kwarg(attribute))
        kwargs["domain"] = ms_domain

        qembed_layer_norm_node = onnx.helper.make_node("QEmbedLayerNormalization", 
                                                       inputs, node.output,
                                                       node.name, **kwargs)
        self.quantizer.new_nodes.append(qembed_layer_norm_node)
        self.quantizer.remove_nodes.extend(parents)