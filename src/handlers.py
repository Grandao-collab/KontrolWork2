from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db import users, tasks
from src.keyboards import get_tasks_keyboard

router = Router()

# Состояния для FSM
class TaskStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_done_id = State()
    waiting_for_delete_id = State()

# --- /start ---
@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    username = user.username or "unknown"
    first_name = user.first_name or "пользователь"

    users.register_user(user.id, username)
    await message.answer(f"Привет, {first_name}! Я твой личный трекер задач. Используй меню команд.")

# --- /add (FSM) ---
@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("Введите название новой задачи:")
    await state.set_state(TaskStates.waiting_for_title)

@router.message(TaskStates.waiting_for_title)
async def process_task_title(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    text = message.text
    if not text:
        await message.answer("Пустое сообщение. Введите название задачи.")
        return

    tasks.add_task(user.id, text)
    await message.answer(f"✅ Задача «{text}» успешно добавлена!")
    await state.clear()

# --- /tasks ---
@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    user_tasks = tasks.get_tasks(user.id)
    if not user_tasks:
        await message.answer("У вас пока нет задач.")
        return
    
    text = "📋 Ваш список задач:\n\n"
    for task_id, title, is_done in user_tasks:
        status = "✅" if is_done else "⬜"
        text += f"{status} №{task_id} — {title}\n"
    
    kb = get_tasks_keyboard(user_tasks)
    await message.answer(text, reply_markup=kb)

# --- /done через FSM ---
@router.message(Command("done"))
async def cmd_done(message: Message, state: FSMContext):
    await message.answer("Введите порядковый номер (ID) задачи, которую хотите выполнить:")
    await state.set_state(TaskStates.waiting_for_done_id)

@router.message(TaskStates.waiting_for_done_id)
async def process_done_id(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    text = message.text or ""
    if not text.isdigit():
        await message.answer("Ошибка: введите корректное число!")
        return
        
    task_id = int(text)
    success = tasks.complete_task(task_id, user.id)
    
    if success:
        await message.answer(f"🎉 Задача №{task_id} отмечена как выполненная!")
        await state.clear()
    else:
        await message.answer("❌ Ошибка: задача не найдена или принадлежит не вам. Попробуйте еще раз.")

# --- /done через Inline-кнопку ---
@router.callback_query(lambda c: c.data and c.data.startswith("done_"))
async def callback_done(callback: CallbackQuery):
    user = callback.from_user
    if user is None:
        await callback.answer("Не удалось определить пользователя", show_alert=True)
        return

    data = callback.data or ""
    task_id = int(data.split("_")[1])
    success = tasks.complete_task(task_id, user.id)
    
    if success:
        await callback.answer("Задача выполнена!")
        # Обновляем список задач на месте
        user_tasks = tasks.get_tasks(user.id)
        text = "📋 Ваш список задач:\n\n"
        for t_id, title, is_done in user_tasks:
            status = "✅" if is_done else "⬜"
            text += f"{status} №{t_id} — {title}\n"
        
        if isinstance(callback.message, Message):
            await callback.message.edit_text(text, reply_markup=get_tasks_keyboard(user_tasks))
        else:
            await callback.answer("Не удалось обновить список задач", show_alert=True)
    else:
        await callback.answer("Ошибка выполнения", show_alert=True)

# --- /delete (Дополнительное требование) ---
@router.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext):
    await message.answer("Введите номер задачи, которую хотите удалить:")
    await state.set_state(TaskStates.waiting_for_delete_id)

@router.message(TaskStates.waiting_for_delete_id)
async def process_delete_id(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    text = message.text or ""
    if not text.isdigit():
        await message.answer("Ошибка: введите число!")
        return
        
    task_id = int(text)
    success = tasks.delete_task(task_id, user.id)
    
    if success:
        await message.answer(f"🗑️ Задача №{task_id} удалена.")
        await state.clear()
    else:
        await message.answer("❌ Ошибка: задача не найдена. Попробуйте еще раз.")

# --- /stats ---
@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    stats = tasks.get_user_stats(user.id)
    if not stats:
        await message.answer("📊 Статистика пуста. Сначала добавьте задачи.")
        return
        
    total, done, undone = stats
    # Если SUM вернул None, превращаем в 0
    done = done or 0
    undone = undone or 0
    
    await message.answer(
        f"📊 Ваша статистика:\n"
        f"Всего задач: {total}\n"
        f"Выполнено: {done} ✅\n"
        f"Не выполнено: {undone} ⬜"
    )