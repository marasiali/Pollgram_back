from django.shortcuts import render
from dj_rest_auth.registration.views import ConfirmEmailView
from django.shortcuts import reverse

def verified(request):
    return render(request, 'pollgram_auth/confirmEmail.html')


class CustomConfirmEmailView(ConfirmEmailView):
    def get_redirect_url(self):
        return reverse('account_email_verified')