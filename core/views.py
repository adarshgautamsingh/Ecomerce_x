from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Category, Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

def category(request,foo):
    foo=foo.replace('-',' ')
    
    try:
         category=Category.objects.get(name=foo)
         products=Product.objects.filter(category=category)
         return render(request,'category.html',{'products':products,'category':category})
    except:
          messages.success(request, "This category doesn't exist!") 
          return redirect('index')  



def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})


def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] # Corrected accessing request.POST
        password = request.POST['password']  # Corrected accessing request.POST
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('index')
        else:
            messages.success(request, "There was an error!")
            return redirect('login')   
    else:
        return render(request, 'login.html', {})
def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out....Thanks!"))
    return redirect('index')  # Redirect to the desired URL after logout

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully registered!")
            return redirect('index')
        else:
            messages.success(request, "Oops! There was a problem registering your account. Please try again.")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
