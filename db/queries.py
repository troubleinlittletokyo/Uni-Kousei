from sqlalchemy import select, update
from db.database import async_session
from db.models import User

#create user
async def get_or_create_user(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()
        return user

#update user
async def update_user(tg_id, university, faculty, course, group_name, subgroup):
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, tg_id)
            if not user:
                user = User(tg_id=tg_id)
                session.add(user)
            
            user.university = university
            user.faculty = faculty
            user.course = course
            user.group_name = group_name
            user.subgroup = subgroup 

#daily schedule time check
async def get_users_by_time(current_time: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(
                User.daily_schedule == True,
                User.daily_schedule_time == current_time
            )
        )
        return result.scalars().all()

#update daily schedule ON\OFF
async def update_user_daily_schedule(tg_id: int, new_status: bool):
    async with async_session() as session:
        async with session.begin():
            stmt = (
                update(User).where(User.tg_id == tg_id).values(daily_schedule=new_status)
            )
            await session.execute(stmt)

#update notification ON\OFF
async def update_user_notification(tg_id: int, new_status: bool):
    async with async_session() as session:
        async with session.begin():
            stmt = (
                update(User).where(User.tg_id == tg_id).values(notifications_lessons=new_status)
            )
            await session.execute(stmt)

async def update_user_settings(tg_id: int, **kwargs):
    async with async_session() as session:
        async with session.begin():
            stmt = update(User).where(User.tg_id == tg_id).values(**kwargs)
            await session.execute(stmt)