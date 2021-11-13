from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.models import User
from .forms import UpdateProfileForm,UpdateUserForm,SignUpForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required 
def profile_view(request):
    confirm=False
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            confirm=True

    user = User.objects.get(id=request.user.id)
    profile =Profile.objects.get(user=request.user)
    context={
        "user":user,
        "profile":profile,
        # "form":profile_form,
        # "user_form":user_form,
        "confirm":confirm,
        }
    return render(request, 'profiles/profile.html', context)
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    error_message=None
    form=AuthenticationForm()
    form_signup = UserCreationForm()
    if request.method=="POST":
        submit_type=request.POST.get('submit_type')
        
        if submit_type=='login':
            form=AuthenticationForm(data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    if request.GET.get("next"):
                        return redirect(request.GET.get("next"))
                    else:
                        return redirect("sales:index")
            else:
                error_message=form.non_field_errors 
        elif submit_type=='register':
            print("weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            form_signup = UserCreationForm(request.POST)
            if form_signup.is_valid():
                form_signup.save()
                username = form_signup.cleaned_data.get('username')
                raw_password = form_signup.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("sales:index")
            else:
                error_message=form_signup.errors
            print("error message:",error_message)
            
            
    context={
        "form":form,
        "form_signup":form_signup,
        "error_message":error_message
    }
    return render(request,"auth/login.html", context)
        
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form_signup': form})