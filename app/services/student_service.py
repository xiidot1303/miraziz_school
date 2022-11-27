from app.models import Student
from app.services import *
from django.db.models import Exists, OuterRef

def all_students():
    query = Student.objects.all()
    return query

def get_student_by_pk(pk):
    obj = get_object_or_404(Student, pk=pk)
    return obj

def filter_students_who_are_not_in_group(group):
    students = Student.objects.filter(
        ~Exists(group.members.filter(student_id=OuterRef('pk'))), 
        status=1
        )
    return students

def filter_students_who_are_member_of_group(group):
    students = Student.objects.filter(
        Exists(group.members.filter(student_id=OuterRef('pk'))), 
        status=1
        )
    return students

