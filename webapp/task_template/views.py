import logging

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.task_template.forms import TaskTemplateForm
from webapp.task_template.models import Reminder, TaskTemplate
from webapp.todo.models import Task

blueprint = Blueprint("task_template", __name__, url_prefix="/templates")


@blueprint.route("/")
def list_templates():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    task_templates = TaskTemplate.query.filter_by(owner=current_user.id).all()
    title = "Все задачи"
    return render_template(
        "task_template/list.html", page_title=title, task_templates=task_templates
    )


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_template():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = TaskTemplateForm()
    title = "Новая задача"
    return render_template("task_template/add.html", page_title=title, form=form)


@blueprint.route("/process-save-template", methods=["POST"])
def process_save_template():
    form = TaskTemplateForm()
    if form.validate_on_submit():
        new_task_template = TaskTemplate(
            name=form.name.data,
            description=form.description.data,
            owner=current_user.id,
        )
        db.session.add(new_task_template)
        db.session.commit()
        logging.info(f"{new_task_template} created")

        new_task = Task(date_id=current_user.active_date, task_template_id=new_task_template.id)
        db.session.add(new_task)

        if form.to_time.data:
            new_time = Reminder(
                task_template_id=new_task_template.id, reminder_time=form.to_time.data
            )
            db.session.add(new_time)
        db.session.commit()

        logging.info(f"{new_task} created")
        if form.to_time.data:
            logging.info(f"{new_time} created")
        flash("Задача добавлена!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
    return redirect(url_for("task_template.add_template"))


@blueprint.route("/edit/<int:task_id>")
@login_required
def edit_template(task_id):
    form = TaskTemplateForm()
    title = f"Редактирование задачи {task_id}"
    return render_template("task_template/edit.html", page_title=title, form=form)


# @blueprint.route("/update/<int:task_id>", methods=["GET", "POST"])
# @login_required
# def update(task_id):
#     task = TaskTemplate.query.filter_by(id=task_id).first()
#     # if task.owner != current_user.id:
#     #     abort(403)
#     task.is_active = not task.is_active
#     db.session.commit()
#     return redirect(url_for("tasks.index"))
