from django.shortcuts import render
from first_app.forms import UserForm,UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
x=''
def index(request):
    return render(request,'first_app/index.html')

def registration(request):
    registered=False
    if request.method=='POST':
        userform=UserForm(data=request.POST)
        userinfoform=UserInfoForm(data=request.POST)

        if userform.is_valid() and userinfoform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()

            userinfo=userinfoform.save(commit=False)
            userinfo.user=user
            if 'profile_pic' in request.FILES:
                userinfo.profile_pic=request.FILES['profile_pic']
            userinfo.save()
            registered=True
        else:
            print(userform.errors,userinfoform.errors)
    else:
        userform=UserForm()
        userinfoform=UserInfoForm()
    return render(request,'first_app/registration.html',{
                            'userform':userform,
                            'userinfoform':userinfoform,
                            'registered':registered})

def user_login(request):
    global x
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        x=username
        user=authenticate(username=username,password=password)
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('special'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'first_app/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    global x
    return HttpResponse('Welcome {}'.format(x))
