from instorage.groups.group import (
    DeleteGroupResponse,
    DeletionInfo,
    GroupInDB,
    GroupMetadata,
    GroupPublicWithMetadata,
)


def to_group_public_with_metadata(group: GroupInDB, num_info_blobs: int):
    return GroupPublicWithMetadata(
        **group.model_dump(), metadata=GroupMetadata(num_info_blobs=num_info_blobs)
    )


def to_groups_public_with_metadata(groups: list[GroupInDB], counts: list[int]):
    return [
        to_group_public_with_metadata(group, count)
        for group, count in zip(groups, counts)
    ]


def to_deletion_response(group: GroupInDB, num_info_blobs: int, success: bool):
    return DeleteGroupResponse(
        **to_group_public_with_metadata(group, num_info_blobs).model_dump(),
        deletion_info=DeletionInfo(success=success)
    )
