from django.shortcuts import render
from wagtail.admin import messages
from wagtail.models import Page
from .forms import EmailForm

def mailing_view(request):
    pages = Page.objects.live().specific()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # Ici, implémentez la logique pour envoyer l'email
            messages.success(request, "L'email a été envoyé avec succès.")
            # Redirigez ou traitez comme nécessaire
    else:
        form = EmailForm()
    return render(request, 'mailing/mailing_form.html', {'pages': pages, 'form': form})
