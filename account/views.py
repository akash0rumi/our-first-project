from django.shortcuts import render, redirect
from .forms import user_form, user_profile_info_form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.

def index(request):
    return render(request, 'account/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        User_Form = user_form(request.POST)
        profile_form = user_profile_info_form(request.POST)

        if User_Form.is_valid() and profile_form.is_valid():
            user = User_Form.save( commit = False)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = profile_form.save( commit = False )
            profile.user = user


            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = User_Form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()


            registered = True


    else:
        User_Form = user_form()
        profile_form = user_profile_info_form()

    my_dict = {
            'registered':registered,
            'User_Form':User_Form,
            'profile_form':profile_form
    }
    return render(request, 'account/registration.html', my_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print("Wrong LOgin DATA provided")
    return render(request,'account/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



@login_required
def user_profile(request):
    return render(request, 'account/user_profile.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
