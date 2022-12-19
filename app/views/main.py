from app.views import *
from app.services.user_service import *
from app.services.language_service import *

@login_required
def main_menu(request):
    if is_superuser(request):
        return redirect('user_list')
    elif is_user_in_group(request, 'teacher'):
        return redirect('lesson_page')
    elif is_user_in_group(request, 'accounter'):
        return redirect('accounter_page')
    elif is_user_in_group(request, 'receptionist'):
        return redirect('student_list_all')
    elif is_user_in_group(request, 'director'):
        return redirect('finance_incomes')

@login_required
def change_lang(request, lang):
    ip = get_user_ip(request)
    update_lang_by_ip(ip, int(lang))
    return redirect_back(request)