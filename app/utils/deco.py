from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.conf import settings
from app.services.teacher_service import *
from app.services.lesson_service import *
from app.services.user_service import *

def go_to_login(request):
    path = request.get_full_path()
    return redirect_to_login(path)

def group_required(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if is_user_in_group(request, *groups):
                return function(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

def check_lesson_teacher_is_user(action):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            teacher = get_teacher_by_user(request.user)
            if action == 'lesson_end':
                pk = kwargs['pk']
                lesson = get_lesson_by_id(pk)
            elif action == 'attendance_change':
                pk = kwargs['pk']
                lesson = get_lesson_by_journal(journal_id=pk)

            if lesson.group.teacher == teacher and lesson.start_datetime != None and lesson.end_datetime == None:
                return function(request, *args, **kwargs)

            return go_to_login(request)
        return wrapper
    return decorator