from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/"
        return path.format(username=request.user.username)
