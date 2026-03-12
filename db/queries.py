from sqlalchemy import select
from db.database import async_session
from db.models import User

async def get_or_create_user(tg_id: int):
    async with async_session() as session:
        statement = select(User).where(User.tg_id == tg_id)

        result = await session.execute(statement)
        
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()
            return user, True
        
        return user, False