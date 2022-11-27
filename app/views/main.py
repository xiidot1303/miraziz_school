from app.views import *
from app.services.user_service import *

@login_required
def main_menu(request):
    if is_superuser(request):
        return redirect('user_list')
    elif is_user_in_group(request, 'teacher'):
        return redirect('lesson_page')
    elif is_user_in_group(request, 'accounter'):
        return redirect('accounter_page')