import httpx
from config import EMOJI_DONE, EMOJI_TODO, WEB, WEB_PARAM, Task
from emoji import emojize
from keyboards import task_inline_keyboard, task_list_inline_keyboard


def get_text_tasks(task_list: list[Task]) -> str:
    """function generates the message text from the task_list"""
    text: str = "Задачи на сегодня:\n\n"
    for index, task in enumerate(task_list, start=1):
        text += str(index)

        if task.task_done:
            text += f' {emojize(EMOJI_DONE, language="alias")} {task.time} ~{task.name}~\n'
        else:
            text += f' {emojize(EMOJI_TODO, language="alias")} {task.time} {task.name}\n'
    text += "\nВыберите номер задачи для просмотра"
    return text


def get_text_task(task: Task) -> str:
    """function generates message text for one task"""
    text: str = f"*{task.name}*\n\n"
    if task.task_done:
        text += f' {emojize(EMOJI_DONE, language="alias")} Завершено\n'
    else:
        text += f' {emojize(EMOJI_TODO, language="alias")} Выполнить\n'
    text += "Время \-" + f"{task.time}\n" if task.time else "Не задано\n"
    text += f"{task.description}"
    return text


def get_task_list(user: str):
    """Checks the request for errors and returns the message text and keyboard for the task list"""
    request: dict = httpx.get(WEB + WEB_PARAM.format(user)).json()
    error = request.get("error")
    if not error:
        task_list: list[Task] = [Task(**task) for task in request["tasks"]]
        text = get_text_tasks(task_list)
        keyboard = task_list_inline_keyboard(task_list)
    else:
        text = error
        keyboard = None
    return (text, keyboard)


def get_task(request):
    """Checks the request for errors and returns the message text and keyboard for one task"""
    error = request.get("error")
    if not error:
        task: Task = Task(**request["task"])
        text = get_text_task(task)
        keyboard = task_inline_keyboard(task)
    else:
        text = error
        keyboard = None
    return (text, keyboard)
