from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AcccountAuthenticationForm, AccounUpdateForm
from content.models import ContentPost

def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            print(form.errors)
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AcccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = AcccountAuthenticationForm()

    context['login_form'] = form

    return render(request,"account/login.html", context)

def account_view(request):

    if not request.user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = AccounUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username']
            }
            form.save()
            context['Success_message'] = "Updated Successfully"
    else:
        form = AccounUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    context['update_form'] = form

    content_posts = ContentPost.objects.filter(author=request.user)
    context['content_posts'] = content_posts

    return render(request, "account/account.html", context)

def must_authenticate_view(request):
    return render(request, "account/must_authenticate.html", {})