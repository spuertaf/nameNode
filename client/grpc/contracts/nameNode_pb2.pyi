from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class add2IndexRequest(_message.Message):
    __slots__ = ["dataNodeIP", "path2Add"]
    DATANODEIP_FIELD_NUMBER: _ClassVar[int]
    PATH2ADD_FIELD_NUMBER: _ClassVar[int]
    dataNodeIP: str
    path2Add: str
    def __init__(self, dataNodeIP: _Optional[str] = ..., path2Add: _Optional[str] = ...) -> None: ...

class add2IndexResponse(_message.Message):
    __slots__ = ["statusCode"]
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    statusCode: int
    def __init__(self, statusCode: _Optional[int] = ...) -> None: ...
