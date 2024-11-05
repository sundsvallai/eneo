# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from fastapi import Depends

from instorage.main.container.container import Container
from instorage.server.dependencies.container import get_container


def get_predefined_roles_service(
    container: Container = Depends(get_container()),
):
    return container.predefined_role_service()
