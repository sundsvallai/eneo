from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from instorage.groups.group import GroupInDBBase
from instorage.main.models import DateTimeModelMixin, InDBOnlyUuid


class InfoBlobBase(BaseModel):
    text: str


class InfoBlobMetadataUpsertPublic(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None


class InfoBlobMetadata(InfoBlobMetadataUpsertPublic):
    embedding_model: str
    size: int


class InfoBlobAdd(InfoBlobBase, InfoBlobMetadataUpsertPublic):
    size: Optional[int] = None
    user_id: int
    group_id: UUID


class InfoBlobAddToDB(InfoBlobAdd):
    id: str
    embedding_model: str
    group_id: int


class InfoBlobUpdatePublic(BaseModel):
    metadata: InfoBlobMetadataUpsertPublic


class InfoBlobUpdate(InfoBlobMetadataUpsertPublic):
    id: str
    user_id: int


class InfoBlobInDBNoText(DateTimeModelMixin):
    id: str
    uuid: UUID
    url: Optional[str] = None
    title: Optional[str] = None
    embedding_model: str
    user_id: int
    size: int

    group: GroupInDBBase

    model_config = ConfigDict(from_attributes=True)


class InfoBlobInDB(InfoBlobInDBNoText):
    text: str


class InfoBlobAddPublic(InfoBlobBase):
    metadata: InfoBlobMetadataUpsertPublic = None


class InfoBlobPublicNoText(BaseModel):
    id: str
    metadata: InfoBlobMetadata
    group_id: UUID


class InfoBlobPublic(InfoBlobPublicNoText):
    text: str


class InfoBlobMetadataFilterPublic(BaseModel):
    group_ids: Optional[list[UUID]] = None
    title: Optional[str] = None


class InfoBlobMetadataFilter(InfoBlobMetadataFilterPublic):
    user_id: Optional[int] = None
    group_ids: Optional[list[int]] = None


class InfoBlobChunk(BaseModel):
    info_blob_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    user_id: int
    text: str
    chunk_no: int


class InfoBlobChunkWithEmbedding(InfoBlobChunk):
    embedding: list[float]


class InfoBlobChunkInDataStore(InfoBlobChunk):
    id: str


class InfoBlobChunk2(BaseModel):
    text: str
    chunk_no: int
    info_blob_id: UUID
    info_blob_old_id: str


class InfoBlobChunkWithEmbedding2(InfoBlobChunk2):
    embedding: list[float]


class InfoBlobChunkInDB(InDBOnlyUuid, InfoBlobChunkWithEmbedding2):
    pass


class InfoBlobChunkInDBWithScore(InfoBlobChunkInDB):
    score: float


class ChunkWithInfoBlobId(InfoBlobChunkInDBWithScore):
    info_blob_str_id: str


class InfoBlobChunkWithScore(InfoBlobChunkInDataStore):
    score: float


class Query(BaseModel):
    query: str
    top_k: int = 30


class QueryWithEmbedding(Query):
    embedding: list[float]
