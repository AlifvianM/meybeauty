from django.http import HttpResponse
from django.shortcuts import render
from .forms import ProfileForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileForm, MyAuthForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('shop-list')
        # ...
    else:
        # messages.danger("Akun tidak dapat masuk")
        return redirect('register')
        # ...

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST)
        a_form = MyAuthForm
        if form.is_valid() and p_form.is_valid():
        	user = form.save(commit=False)
        	user.is_active = True
        	user.save()
        	profile = p_form.save(commit=False)
        	profile.user = user
        	profile.save()
        	new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
        	login(request, new_user)
        	return redirect('shop-list')

            # user = form.save(commit=False)
            # user.is_active = False
            # user.save()
            # profile = p_form.save(commit=False)
            # profile.user = user
            # profile.save()
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your blog account.'
            # message = render_to_string('users/acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activation_token.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #             mail_subject, message, to=[to_email]
            # )
            # email.send()
            # # return HttpResponse('Please confirm your email address to complete the registration')
            # return redirect('shop-list')
    else:
        form = UserRegisterForm()
        p_form = ProfileForm()
        a_form = MyAuthForm()

    return render(request, 'users/login-register.html', {'form': form, 'p_form':p_form, 'a_form':a_form})


def signup(request):
    if request.method == 'POST':
        a_form = MyAuthForm(request.POST)
        form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            return redirect('register_success')
    else:
        a_form = MyAuthForm()
        form = UserRegisterForm()
        p_form = ProfileForm()
    return render(request, 'users/login-register.html', {'a_form':a_form, 'form': form, 'p_form':p_form})

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
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('register')
    else:
        return HttpResponse('Activation link is invalid!')

def register_success(request):
    return render(request, 'users/register_success.html')


