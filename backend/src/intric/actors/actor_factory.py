from typing import TYPE_CHECKING

from intric.actors.actors.space_actor import SpaceActor

if TYPE_CHECKING:
    from intric.spaces.space import Space
    from intric.users.user import UserInDB


class ActorFactory:
    @staticmethod
    def create_space_actor(user: "UserInDB", space: "Space"):
        return SpaceActor(user=user, space=space)
