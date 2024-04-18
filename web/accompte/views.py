import datetime
from django.core.files.images import get_image_dimensions
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.contrib import messages

from utils.variables import TIMEZONES, LANGUAGES, THEMES, CIVILITIES
from allauth.account.views import PasswordChangeView

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def handle_no_permission(self):
        messages.info(self.request, "Veuillez vous connecter pour changer votre mot de passe.")
        return redirect(f"{reverse('account_login')}?next={self.request.get_full_path()}")

    def get_success_url(self):        
        return reverse_lazy('account_profile')


def profile_view(request):
    civilities = CIVILITIES
    timezones = TIMEZONES
    languages = LANGUAGES
    themes = THEMES
    
    
    return render(request, "account/profile.html", {
        'civilities': civilities,
        'timezones': timezones,
        'languages': languages,
        'themes': themes,
    })


@login_required
def profile_update(request):
    user = request.user
    user_profile = user.wagtail_userprofile
    
    if request.method == 'POST':
        
        redirect_to = 'account_profile'
        next_url = request.POST.get('next', None)
        print(next_url)
        
        if next_url:
            redirect_to = next_url
        
        print(redirect_to)
        
        user_profile.theme = request.POST.get('theme', user_profile.theme)
        user_profile.preferred_language = request.POST.get('preferred_language', user_profile.preferred_language)
        user_profile.current_time_zone = request.POST.get('current_time_zone', user_profile.current_time_zone)
        
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        if date_of_birth:
            try:
                user.date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, _("Le format de la date n'est pas valide. Le format correct est AAAA-MM-JJ."))
                return render(request, 'account/profile.html', {'user_profile': user_profile, 'user': user})
        else:
            user.date_of_birth = None 

        civility = request.POST.get('civility', user.civility)
        mobile_phone = request.POST.get('mobile_phone', user.mobile_phone)
        address1 = request.POST.get('address1', user.address1)
        address2 = request.POST.get('address2', user.address2)
        zip_code = request.POST.get('zip_code', user.zip_code)
        city = request.POST.get('city', user.city)

        print(date_of_birth)
        
        user.civility = civility
        user.mobile_phone = mobile_phone
        user.address1 = address1
        user.address2 = address2
        user.zip_code = zip_code
        user.city = city
                
        if 'clear_avatar' in request.POST and request.POST['clear_avatar'] == 'on':
            user_profile.avatar.delete(save=True)
                    
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            print(avatar_file)
            print(type(avatar_file))
            if avatar_file.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
                messages.error(request, _('Uploaded file is not a valid image. Only JPEG, PNG, and WEBP formats are accepted.'))
                return render(request, 'account/profile.html', {
                    'user_profile': user_profile,
                    'user': user
                })

            # Vérification et sauvegarde de l'image
            try:
                w, h = get_image_dimensions(avatar_file)
                print(w, h)
                max_width = max_height = 2000
                if w is None or h is None or w > max_width or h > max_height:
                    raise ValueError(_('Please use an image that is {0} x {1} pixels or smaller.').format(max_width, max_height))

                max_size = 5 * 1024 * 1024  # 5 MB
                if avatar_file.size > max_size:
                    raise ValueError(_('Please keep filesize under {0}. Current filesize {1}').format(filesizeformat(max_size), filesizeformat(avatar_file.size)))

                user_profile.avatar.save(avatar_file.name, avatar_file, save=True)

            except ValueError as e:
                messages.error(request, str(e))
                return render(request, 'account/profile.html', {
                    'user_profile': user_profile,
                    'user': user
                })
        
        # Sauvegarder les modifications non relatives à l'image
        user.save()
        user_profile.save()
        
        messages.success(request, _("Profile updated successfully."))
        return redirect(redirect_to)
    
    else:
        return render(request, 'account/profile.html', {
            'user_profile': user_profile,
            'user': user
        })