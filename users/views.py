from django.shortcuts import render
from .forms import ProfileForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileForm, MyAuthForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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

