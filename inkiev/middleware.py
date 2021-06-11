from django.http import Http404


def return_admin_or_404(next_):
    """
    Скрывает админку от всех у кого нет доступа
    """
    def middleware(request):
        if not request.user.is_staff and request.path.startswith('/admin'):
            raise Http404()
        else:
            response = next_(request)
            return response

    return middleware
