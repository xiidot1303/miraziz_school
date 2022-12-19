from app.models import (
    Group,
    Group_member, 
    Lesson, 
    add_student_to_lessons as _add_student_to_lessons
)
from app.services import *
from app.services.payment_service import (
    calculate_monthly_payment as _calculate_monthly_payment,
    calculate_full_payment as _calculate_full_payment
)

def all_groups():
    query = Group.objects.all()
    return query

def get_group_by_pk(pk):
    obj = get_object_or_404(Group, pk=pk)
    return obj

def check_group_has_lesson(obj):
    lessons = Lesson.objects.filter(group=obj)
    if lessons:
        return True
    else:
        return False

def check_teacher_has_lesson(data, obj):
    teacher, weekdays, start_time, end_time = data.get('teacher'), data.get('weekdays'), data.get('start_time'), data.get('end_time')
    query = Group.objects.filter(
        start_time__lte=end_time, end_time__gte=start_time, teacher=teacher
        ).exclude(
            pk=obj.pk
        )   
    for group in query:
        if group.weekdays.all() & weekdays.all():
            return True
    else:
        return False

def filter_groups_that_today_has_lesson():
    now = datetime_now()
    weekday = now.weekday()
    query = Group.objects.filter(
        weekdays__day = weekday, start_date__lte=today(), status=1
    ).exclude(remaining_lessons=0)
    return query

def add_student_to_group(group, student, payment_method, discount, start_date=today()):
    # start_date = today() if not start_date else start_date
    group.members.get_or_create(student=student)
    group.save()
    if payment_method == 'monthly':
        # calculate monthly payment
        _calculate_monthly_payment(group, student, start_date, discount)
    else:
        _calculate_full_payment(group, student, start_date, discount)

    _add_student_to_lessons(student)



def get_group_by_payment(payment):
    group = Group.objects.get(members__payments=payment)
    return group

# GROUP MEMBERS

def create_group_member(student):
    obj = Group_member.objects.create(student=student)
    return obj

def get_group_member_by_pk(pk):
    obj = get_object_or_404(Group_member, pk=pk)
    return obj

def delete_group_member(member=None, member_pk=None):
    member = get_group_member_by_pk(member_pk) if not member else member    
    member.delete()

def filter_group_members_by_student(student):
    query = Group_member.objects.filter(student=student)
    return query