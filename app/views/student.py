from app.views import *
from app.services.student_service import *
from app.services.group_service import *

@login_required
@permission_required('app.view_student')
def student_list_all(request):
    students = all_students()
    context = {'students': students}
    return render(request, 'student/student_list_all.html', context)

@login_required
@permission_required('app.view_student')
def student_page(request, pk):
    student = get_student_by_pk(pk)
    group_members = filter_group_members_by_student(student)
    context = {'student': student, 'group_members': group_members}
    return render(request, 'student/student_page.html', context)

class StudentEditView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'app.change_student'
    form_class = StudentForm
    model = Student
    template_name = 'main/edit.html'
    # success_url = reverse_lazy('student_list_all')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        student = context['object']
        context['title'] = 'student | changing'
        context['header1'] = 'student'
        context['header2'] = student.name
        return context
    
    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, text_successfully_changed(self.request))
        return reverse_lazy('student_list_all')

class StudentCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ['app.add_student']
    form_class = StudentForm
    model = Student
    template_name = 'main/create.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'student | creating'
        context['header1'] = 'student'
        context['header2'] = 'creating'
        return context

    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, text_successfully_created(self.request))
        return reverse_lazy('student_list_all')

@permission_required('app.delete_student')
@login_required
def student_delete(request, pk):
    student = get_student_by_pk(pk)
    try:
        student.delete()
        messages.success(request, text_successfully_deleted(request))
        return redirect(student_list_all)
    except:
        # student.status = 0
        # student.save()
        # messages.success(request, text_successfully_deleted(request))
        messages.warning(request, text_can_not_delete_sth(request, sth='student', bcoz='group'))
        return redirect_back(request)