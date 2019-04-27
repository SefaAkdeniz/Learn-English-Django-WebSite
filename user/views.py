from django.shortcuts import render,redirect
from user.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username =username)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.success(request,"Başarıyla Kayıt Oldunuz...")
        return redirect("index")
    context = {
            "form" : form
        }
    return render(request,"register.html",context)

def loginUser(request):
    return render(request,"login.html")
def logoutUser(request):
    pass
 