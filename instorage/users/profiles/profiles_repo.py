from instorage.users.profiles.profile import ProfileCreate, ProfileInDB, ProfileUpdate
from instorage.users.user import UserInDB

CREATE_PROFILE_FOR_USER_QUERY = """
    INSERT INTO profiles (full_name, image, user_id)
    VALUES (:full_name, :image, :user_id)
    RETURNING id, full_name, image, user_id, created_at, updated_at;
"""

GET_PROFILE_BY_USER_ID_QUERY = """
    SELECT id, full_name, image, user_id, created_at, updated_at
    FROM profiles
    WHERE user_id = :user_id;
"""

GET_PROFILE_BY_USERNAME_QUERY = """
    SELECT p.id,
           u.email AS email,
           u.username AS username,
           full_name,
           image,
           user_id,
           p.created_at,
           p.updated_at
    FROM profiles p
        INNER JOIN users u
        ON p.user_id = u.id
    WHERE user_id = (SELECT id FROM users WHERE username = :username);
"""

UPDATE_PROFILE_QUERY = """
    UPDATE profiles
    SET full_name    = :full_name,
        image        = :image
    WHERE user_id = :user_id
    RETURNING id, full_name, image, user_id, created_at, updated_at;
"""


class ProfilesRepository:
    def __init__(self, db):
        self.db = db

    async def create_profile_for_user(
        self, *, profile_create: ProfileCreate
    ) -> ProfileInDB:
        created_profile = await self.db.fetch_one(
            query=CREATE_PROFILE_FOR_USER_QUERY, values=profile_create.dict()
        )
        return created_profile

    async def get_profile_by_user_id(self, *, user_id: int) -> ProfileInDB:
        profile_record = await self.db.fetch_one(
            query=GET_PROFILE_BY_USER_ID_QUERY, values={"user_id": user_id}
        )
        if not profile_record:
            return None
        return ProfileInDB(**profile_record)

    async def get_profile_by_username(self, *, username: str) -> ProfileInDB:
        # Check database if user exists
        # If we have a user, grab the email and username
        # and attached it to the profile
        profile_record = await self.db.fetch_one(
            query=GET_PROFILE_BY_USERNAME_QUERY, values={"username": username}
        )
        if profile_record:
            return ProfileInDB(**profile_record)

    async def update_profile(
        self, *, profile_update: ProfileUpdate, requesting_user: UserInDB
    ) -> ProfileInDB:
        profile = await self.get_profile_by_user_id(user_id=requesting_user.id)
        update_params = profile.copy(update=profile_update.dict(exclude_unset=True))

        updated_profile = await self.db.fetch_one(
            query=UPDATE_PROFILE_QUERY,
            values=update_params.dict(
                exclude={"id", "created_at", "updated_at", "username", "email"}
            ),
        )
        return ProfileInDB(**updated_profile)
