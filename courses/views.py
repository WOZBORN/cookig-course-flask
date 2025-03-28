from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Enrollment, Course, Lesson
from .forms import EnrollmentForm


def index(request):
    form = EnrollmentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']

        if Enrollment.objects.filter(email=email).exists():
            messages.error(request, 'Этот email уже зарегистрирован. Пожалуйста, используйте другой.')
            return redirect('index')

        if phone and Enrollment.objects.filter(phone=phone).exists():
            messages.error(request, 'Этот номер телефона уже зарегистрирован. Пожалуйста, используйте другой.')
            return redirect('index')

        try:
            form.save()
            messages.success(request, 'Спасибо за запись! Мы свяжемся с вами в ближайшее время.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при сохранении записи: {str(e)}')
            return redirect('index')

    return render(request, 'index.html', {'form': form})


def courses_view(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, 'courses.html', {'courses': courses})


def course_detail(request, course_id, lesson_id=None):
    course = get_object_or_404(Course, pk=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    if not lessons.exists():
        messages.warning(request, 'Для данного курса нет уроков.')
        return redirect('courses')

    if lesson_id is not None:
        current_lesson = lessons.filter(pk=lesson_id).first()
        if not current_lesson:
            messages.warning(request, 'Указанный урок не найден, показываем первый урок.')
            current_lesson = lessons.first()
    else:
        current_lesson = lessons.first()

    context = {
        'course': course,
        'lessons': lessons,
        'current_lesson': current_lesson
    }

    return render(request, 'course_detail.html', context)
