from django.shortcuts import render , redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from authentication.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

def signup_view(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render (request,'signup.html', {'error':'Sorry, Username is already exists'})
            except User.DoesNotExist:
                user = User(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('firstname'),
                    last_name=request.POST.get('lastname'),
                    email=request.POST.get('email'),
                    password= make_password(request.POST.get('password1')),
                    pic = request.FILES.get('pic')
                    )
                user.save()
                auth.login(request,user)
                print(user ,"<-------------------create an account and login successfully")
                return redirect(reverse('room', kwargs={'room_name': 0}))
        else:
            return render (request,'signup.html', {'error':'Sorry, Password does not match'})
    else:
        return render(request,'signup.html')


def login_view(request):
    # user can not open login page if already authenticated
    if request.user.is_anonymous:
        if request.method == 'POST':
            user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
            if user is not None:
                auth.login(request,user)
                print(user , "<-------------------login successfully")
                user.is_online=True
                user.save()
                return redirect(reverse('room', kwargs={'room_name': 0}))        
            else:
                return render (request,'login.html', {'error':'sorry ,invalid credentials. Try again'})
        else:
            return render(request, 'login.html')
    return redirect(reverse('room', kwargs={'room_name': 0}))

    
@login_required    
def logout_view(request):
    user = request.user
    user.is_online=False
    user.save()
    auth.logout(request)
    return redirect('login')
