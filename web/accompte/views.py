from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def handle_no_permission(self):
        messages.info(self.request, "Veuillez vous connecter pour changer votre mot de passe.")
        return redirect(f"{reverse('account_login')}?next={self.request.get_full_path()}")

    def get_success_url(self):        
        return reverse_lazy('account_profile')
