from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    choosing_university = State()
    choosing_faculty = State() 
    choosing_course = State()
    choosing_group = State()
    choosing_subgroup = State()