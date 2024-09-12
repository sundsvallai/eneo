from instorage.main.container.container import Container
from instorage.users.user import UserUpdate


async def setup_user(container: Container):
    user_repo = container.user_repo()

    user_update = UserUpdate(is_active=True)
    await user_repo.update(user=user_update)
