from django.shortcuts import render


def verified(request):
    return render(request, 'pollgram_auth/confirmEmail.html')
# Create your views here.
