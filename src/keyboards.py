from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_tasks_keyboard(tasks) -> InlineKeyboardMarkup:
    """Создает инлайн-кнопки для закрытия задач прямо из списка"""
    buttons = []
    for task_id, title, is_done in tasks:
        if not is_done:
            buttons.append([InlineKeyboardButton(
                text=f"Выполнить №{task_id}", 
                callback_data=f"done_{task_id}"
            )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)