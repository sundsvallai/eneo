from typing import TYPE_CHECKING

from intric.main.exceptions import UnauthorizedException

if TYPE_CHECKING:
    from uuid import UUID

    from intric.actors import ActorManager
    from intric.spaces.space_repo import SpaceRepository
    from intric.spaces.space_service import SpaceService


class ResourceMoverService:
    def __init__(
        self,
        space_service: "SpaceService",
        space_repo: "SpaceRepository",
        actor_manager: "ActorManager",
    ):
        self.space_service = space_service
        self.space_repo = space_repo
        self.actor_manager = actor_manager

    async def move_website_to_space(self, website_id: "UUID", space_id: "UUID"):
        source_space = await self.space_service.get_space_by_website(website_id)
        source_space_actor = self.actor_manager.get_space_actor_from_space(source_space)

        if not source_space_actor.can_delete_websites():
            raise UnauthorizedException("User does not have permission to move website from space")

        target_space = await self.space_service.get_space(space_id)
        target_space_actor = self.actor_manager.get_space_actor_from_space(target_space)

        if not target_space_actor.can_create_websites():
            raise UnauthorizedException(
                "User does not have permission to create websites in the space"
            )

        website = source_space.get_website(website_id)

        target_space.add_website(website)
        source_space.remove_website(website)

        await self.space_repo.update(space=target_space)
        await self.space_repo.update(space=source_space)

    async def move_collection_to_space(self, collection_id: "UUID", space_id: "UUID"):
        source_space = await self.space_service.get_space_by_collection(collection_id)
        source_space_actor = self.actor_manager.get_space_actor_from_space(source_space)

        if not source_space_actor.can_delete_collections():
            raise UnauthorizedException(
                "User does not have permission to move collection from space"
            )

        target_space = await self.space_service.get_space(space_id)
        target_space_actor = self.actor_manager.get_space_actor_from_space(target_space)

        if not target_space_actor.can_create_collections():
            raise UnauthorizedException(
                "User does not have permission to create collections in the space"
            )

        collection = source_space.get_collection(collection_id)

        target_space.add_collection(collection)
        source_space.remove_collection(collection)

        await self.space_repo.update(space=target_space)
        await self.space_repo.update(space=source_space)

    async def move_assistant_to_space(
        self, assistant_id: "UUID", space_id: "UUID", move_resources: bool = False
    ):
        source_space = await self.space_service.get_space_by_assistant(assistant_id)
        source_space_actor = self.actor_manager.get_space_actor_from_space(source_space)

        if not source_space_actor.can_delete_assistants():
            raise UnauthorizedException(
                "User does not have permission to move assistant from space"
            )

        target_space = await self.space_service.get_space(space_id)
        target_space_actor = self.actor_manager.get_space_actor_from_space(target_space)

        if not target_space_actor.can_create_assistants():
            raise UnauthorizedException(
                "User does not have permission to create assistants in the space"
            )

        assistant = source_space.get_assistant(assistant_id)

        target_space.add_assistant(assistant)
        source_space.remove_assistant(assistant)

        if move_resources:
            for collection in assistant.collections:
                if not source_space_actor.can_delete_collections():
                    raise UnauthorizedException(
                        "User does not have permission to move collection from space"
                    )

                if not target_space_actor.can_create_collections():
                    raise UnauthorizedException(
                        "User does not have permission to create collections in the space"
                    )

                target_space.add_collection(collection)
                source_space.remove_collection(collection)

            for website in assistant.websites:
                if not source_space_actor.can_delete_websites():
                    raise UnauthorizedException(
                        "User does not have permission to move website from space"
                    )

                if not target_space_actor.can_create_websites():
                    raise UnauthorizedException(
                        "User does not have permission to create websites in the space"
                    )

                target_space.add_website(website)
                source_space.remove_website(website)

        await self.space_repo.update(space=target_space)
        await self.space_repo.update(space=source_space)
