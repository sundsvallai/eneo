import sqlalchemy as sa

from instorage.admin.beta_keys.beta_key import BetaKeyInDB
from instorage.database.database import AsyncSession
from instorage.database.tables.beta_keys_table import BetaKeys

CREATE_NEW_BETA_KEY_QUERY = """
    INSERT INTO beta_keys (key, used)
    VALUES (:key, :used)
    RETURNING id, key, used, created_at, updated_at
"""

GET_KEY_BY_KEY_QUERY = """
    SELECT id, key, used, created_at, updated_at
    FROM beta_keys
    WHERE key = :key
"""

CONSUME_BETA_KEY_QUERY = """
    UPDATE beta_keys
    SET used = :used
    WHERE key = :key
    RETURNING id, key, used, created_at, updated_at
"""


class BetaKeyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_beta_key(self, beta_key: str) -> BetaKeyInDB:
        stmt = sa.insert(BetaKeys).values(key=beta_key, used=False).returning(BetaKeys)
        result = await self.session.execute(stmt)
        new_beta_key = result.scalar_one()

        return BetaKeyInDB.from_orm(new_beta_key)

    async def get_beta_key(self, beta_key: str) -> BetaKeyInDB:
        stmt = sa.select(BetaKeys).where(BetaKeys.key == beta_key)
        result = await self.session.execute(stmt)
        beta_key_in_db = result.scalar_one_or_none()

        if beta_key_in_db is None:
            return None
        else:
            return BetaKeyInDB.from_orm(beta_key_in_db)

    async def consume_beta_key(self, beta_key: str) -> BetaKeyInDB:
        stmt = (
            sa.update(BetaKeys)
            .values(used=True)
            .where(BetaKeys.key == beta_key)
            .returning(BetaKeys)
        )
        result = await self.session.execute(stmt)

        consumed_beta_key = result.scalar_one()

        return BetaKeyInDB.from_orm(consumed_beta_key)
