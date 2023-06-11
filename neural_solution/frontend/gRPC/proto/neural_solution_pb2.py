# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: neural_solution.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15neural_solution.proto\x12\x0fneural_solution\x1a\x1bgoogle/protobuf/empty.proto\"y\n\x04Task\x12\x12\n\nscript_url\x18\x01 \x01(\t\x12\x11\n\toptimized\x18\x02 \x01(\x08\x12\x11\n\targuments\x18\x03 \x03(\t\x12\x10\n\x08\x61pproach\x18\x04 \x01(\t\x12\x14\n\x0crequirements\x18\x05 \x03(\t\x12\x0f\n\x07workers\x18\x06 \x01(\x05\"<\n\x0cTaskResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07task_id\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\"\x19\n\x06TaskId\x12\x0f\n\x07task_id\x18\x01 \x01(\t\"K\n\nTaskStatus\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x18\n\x10optimized_result\x18\x02 \x01(\t\x12\x13\n\x0bresult_path\x18\x03 \x01(\t\"\x0e\n\x0c\x45mptyRequest\"!\n\x0eWelcomeMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"2\n\x13ResponsePingMessage\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0b\n\x03msg\x18\x02 \x01(\t\"]\n\x12ResponseTaskResult\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x1a\n\x12tuning_information\x18\x02 \x01(\t\x12\x1b\n\x13optimization_result\x18\x03 \x01(\t2\xb5\x02\n\x0bTaskService\x12\x46\n\x04Ping\x12\x16.google.protobuf.Empty\x1a$.neural_solution.ResponsePingMessage\"\x00\x12\x44\n\nSubmitTask\x12\x15.neural_solution.Task\x1a\x1d.neural_solution.TaskResponse\"\x00\x12\x45\n\x0bGetTaskById\x12\x17.neural_solution.TaskId\x1a\x1b.neural_solution.TaskStatus\"\x00\x12Q\n\x0fQueryTaskResult\x12\x17.neural_solution.TaskId\x1a#.neural_solution.ResponseTaskResult\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'neural_solution_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TASK._serialized_start=71
  _TASK._serialized_end=192
  _TASKRESPONSE._serialized_start=194
  _TASKRESPONSE._serialized_end=254
  _TASKID._serialized_start=256
  _TASKID._serialized_end=281
  _TASKSTATUS._serialized_start=283
  _TASKSTATUS._serialized_end=358
  _EMPTYREQUEST._serialized_start=360
  _EMPTYREQUEST._serialized_end=374
  _WELCOMEMESSAGE._serialized_start=376
  _WELCOMEMESSAGE._serialized_end=409
  _RESPONSEPINGMESSAGE._serialized_start=411
  _RESPONSEPINGMESSAGE._serialized_end=461
  _RESPONSETASKRESULT._serialized_start=463
  _RESPONSETASKRESULT._serialized_end=556
  _TASKSERVICE._serialized_start=559
  _TASKSERVICE._serialized_end=868
# @@protoc_insertion_point(module_scope)
