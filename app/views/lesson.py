from app.views import *
from app.services.lesson_service import *
from app.services.teacher_service import *

@login_required
@group_required('teacher')
def lesson_current(request):
    user = request.user
    teacher = get_teacher_by_user(user)
    lesson = get_current_lesson(teacher)
    upcoming_lesson = get_upcoming_lesson(teacher) if not lesson else None
    journal = lesson.journal.all() if lesson else None
    context = {'journal': journal, 'lesson': lesson, 'upcoming_lesson': upcoming_lesson}
    return render(request, 'lesson/lesson_page.html', context)

@login_required
@group_required('teacher')
@check_lesson_teacher_is_user('lesson_end')
def lesson_end(request, pk):
    lesson = get_lesson_by_id(pk)
    if lesson.group.end_time <= time_now() or lesson.group.start_date < today():
        # end lesson 
        lesson.end_datetime = datetime_now()
        lesson.save()
        messages.success(request, get_string('successfully end lesson', request))
    else:
        messages.warning(
            request, 
            get_string('lesson can be finished after {}', request).format(
                lesson.group.end_time.strftime('%H:%M')
            )
            )
    return redirect(lesson_current)


# ATTENDANCE
@login_required
@group_required('teacher')
@check_lesson_teacher_is_user('attendance_change')
def attendance_change(request, pk, status):
    status = True if status == 1 else (False if status == 0 else None)
    change_attend_by_id(pk, status)
    return redirect(lesson_current)
