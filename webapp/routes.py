from flask import Blueprint, render_template, redirect, url_for, flash

from . import db
from .forms import EnrollmentForm
from .models import Enrollment, Course, Lesson

main = Blueprint('main', __name__)

# Главная страница: описание школы, контакты, отзывы и форма записи
@main.route('/', methods=['GET', 'POST'])
def index():
    form = EnrollmentForm()
    if form.validate_on_submit():
        # Проверка, существует ли email или телефон в базе
        existing_email = Enrollment.query.filter_by(email=form.email.data).first()
        existing_phone = Enrollment.query.filter_by(phone=form.phone.data).first() if form.phone.data else None

        if existing_email:
            flash('Этот email уже зарегистрирован. Пожалуйста, используйте другой.')
            return redirect(url_for('main.index'))

        if existing_phone:
            flash('Этот номер телефона уже зарегистрирован. Пожалуйста, используйте другой.')
            return redirect(url_for('main.index'))

        try:
            enrollment = Enrollment(
                fullname=form.fullname.data,
                email=form.email.data,
                phone=form.phone.data
            )
            db.session.add(enrollment)
            db.session.commit()
        except Exception as e:
            flash(f'Произошла ошибка при сохранении записи: {str(e)}')
            return redirect(url_for('main.index'))

        flash('Спасибо за запись! Мы свяжемся с вами в ближайшее время.')
        return redirect(url_for('main.index'))

    return render_template('index.html', form=form)


# Страница со списком курсов по основам готовки
@main.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


# Страница отдельного курса. Если lesson_id не указан, показывается первый урок.
@main.route('/course/<int:course_id>')
@main.route('/course/<int:course_id>/lesson/<int:lesson_id>')
def course_detail(course_id, lesson_id=None):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        flash(f'Курса с id {course_id} не существует.')
    # Получаем уроки курса, отсортированные по порядку
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()

    if not lessons:
        flash('Для данного курса нет уроков.')
        return redirect(url_for('main.courses'))

    # Если lesson_id не передан или урок не найден, выбираем первый урок
    if lesson_id is None:
        current_lesson = lessons[0]
    else:
        current_lesson = Lesson.query.filter_by(id=lesson_id).first()
        if not current_lesson:
            flash('Указанный урок не найден, показываем первый урок.')
            current_lesson = lessons[0]

    return render_template('course_detail.html', course=course, lessons=lessons, current_lesson=current_lesson)
