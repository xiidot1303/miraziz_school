from app.views import *
from app.services.user_service import *

@login_required
def main_menu(request):
    if is_user_in_group(request, 'teacher'):
        return redirect('lesson_page')