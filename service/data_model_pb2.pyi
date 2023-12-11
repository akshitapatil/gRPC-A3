from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class POST_STATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NORMAL: _ClassVar[POST_STATE]
    LOCKED: _ClassVar[POST_STATE]
    HIDDEN: _ClassVar[POST_STATE]

class VoteAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UPVOTE: _ClassVar[VoteAction]
    DOWNVOTE: _ClassVar[VoteAction]
NORMAL: POST_STATE
LOCKED: POST_STATE
HIDDEN: POST_STATE
UPVOTE: VoteAction
DOWNVOTE: VoteAction

class User(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Subreddit(_message.Message):
    __slots__ = ["subreddit_id", "name", "public", "private", "hidden", "tags"]
    SUBREDDIT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    subreddit_id: str
    name: str
    public: bool
    private: bool
    hidden: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, subreddit_id: _Optional[str] = ..., name: _Optional[str] = ..., public: bool = ..., private: bool = ..., hidden: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["post_id", "title", "text", "video_url", "image_url", "author", "score", "state", "publication_date", "subreddit"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    SUBREDDIT_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    title: str
    text: str
    video_url: str
    image_url: str
    author: str
    score: int
    state: POST_STATE
    publication_date: str
    subreddit: Subreddit
    def __init__(self, post_id: _Optional[str] = ..., title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[str] = ..., score: _Optional[int] = ..., state: _Optional[_Union[POST_STATE, str]] = ..., publication_date: _Optional[str] = ..., subreddit: _Optional[_Union[Subreddit, _Mapping]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["comment_id", "text", "author", "score", "hidden", "publication_date", "post_id", "replies_exist"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    REPLIES_EXIST_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    text: str
    author: str
    score: int
    hidden: bool
    publication_date: str
    post_id: str
    replies_exist: bool
    def __init__(self, comment_id: _Optional[str] = ..., text: _Optional[str] = ..., author: _Optional[str] = ..., score: _Optional[int] = ..., hidden: bool = ..., publication_date: _Optional[str] = ..., post_id: _Optional[str] = ..., replies_exist: bool = ...) -> None: ...

class VoteRequest(_message.Message):
    __slots__ = ["action", "post_id", "comment_id"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    action: VoteAction
    post_id: str
    comment_id: str
    def __init__(self, action: _Optional[_Union[VoteAction, str]] = ..., post_id: _Optional[str] = ..., comment_id: _Optional[str] = ...) -> None: ...

class TopCommentsRequest(_message.Message):
    __slots__ = ["post_id", "N", "comment_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    N: int
    comment_id: str
    def __init__(self, post_id: _Optional[str] = ..., N: _Optional[int] = ..., comment_id: _Optional[str] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["entity_id", "score"]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    entity_id: str
    score: int
    def __init__(self, entity_id: _Optional[str] = ..., score: _Optional[int] = ...) -> None: ...
