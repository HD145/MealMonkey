from multiprocessing import context
from re import I
from urllib import response
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .helpers import send_forgot_password_mail
from . models import OrderPost, PersonDetails, Product, PaymentDetail,Profile
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from instamojo_wrapper import Instamojo
from django.conf import settings
from . my_captcha import *
from django.core.mail import send_mail
from django.contrib import messages 

api = Instamojo(api_key=settings.API_KEY,
    auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/'
)
# Create your views here.

def index(request):
    user=request.user
    foods = Product.objects.all()
    return render(request, 'foodfest/index.html', {'foods':foods,'user':user})

def signin(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['name']
        password=request.POST['password']
        # password=request.POST['password']

        user=authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # context={"msg":"Invalid credentials. Please try again"}
            messages.success(request, "Invalid credentials. Please try again")
            return render(request, 'foodfest/signin.html')

    return render(request, 'foodfest/signin.html')

def signup(request):
    if request.method=="POST":
        username = request.POST['name']
        mail = request.POST.get("emailsave")
        password = request.POST['password']
        flag=request.POST.get('g-recaptcha-response')
        # print(flag)
        if flag=="":
            context={'msg':'Recaptcha not verified','captcha':FormWithCaptcha}
            return render(request,'foodfest/signup.html',context)

        if User.objects.filter(username=username):
            context={"msg":"User with this username already exists.", 'captcha':FormWithCaptcha}
            return render(request, 'foodfest/signup.html', context)

        if User.objects.filter(email=mail):
            context={"msg":"User with this email already exists.", 'captcha':FormWithCaptcha}
            return render(request, 'foodfest/signup.html', context)
        else:
            user = User.objects.create_user(username,mail,password)
            user.save()
            messages.success(request, "Your account has been successfully created. Plesase signin to get your account activated")
            return redirect('signin')
    context = {'captcha':FormWithCaptcha}
    return render(request, 'foodfest/signup.html', context)

@csrf_exempt
@login_required(login_url='signin')
def orderpost(request, id):
    food = Product.objects.filter(id=id).first()
    name=food.product_name
    price = food.price
    user = request.user
    
    # print(user)

    foodpost = OrderPost(name=name, price=price, user=user)
    foodpost.save()
    return redirect('index')

@login_required(login_url='signin')
def yourorders(request):
    if request.user.is_authenticated:
        user = request.user
        orders = OrderPost.objects.filter(user=user)
        cost=0
        for order in orders:
            cost = cost+order.price
        return render(request, 'foodfest/yourorders.html', {'orders':orders,'cost':cost})


def deleteorder(request,order_id):
    food = OrderPost.objects.filter(order_id=order_id).first()
    food.delete()
    return redirect('yourorders')

@login_required(login_url='signin')
def vieworder(request,id):
    food = Product.objects.filter(id=id).first()
    return render(request, "foodfest/vieworder.html", {"food":food})

@login_required(login_url='signin')
def search(request):
   
    query=request.GET['query']
    if len(query)>78:
        foods=Product.objects.none()
    else:
        foodname= Product.objects.filter(product_name__icontains=query)
        foodcat= Product.objects.filter(category__icontains=query)
        fooddescription= Product.objects.filter(desc__icontains=query)
        foods= foodname.union(foodcat, fooddescription)
    if foods.count()==0:
        context = {'msg':"No search result found", 'query':query}
        return render(request, 'foodfest/search.html', context)

    params={'foods': foods, 'query': query}
    return render(request, 'foodfest/search.html', params)


def person_details(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            user = request.user
            orders = OrderPost.objects.filter(user=user)
            global cost
            cost=0
            for order in orders:
                cost = cost+order.price
            global person_name
            person_name= request.POST['name']
            phone= request.POST['mobile']
            address= request.POST['address']
            postal= request.POST['postal']
            user=request.user
            details = PersonDetails(person_name=person_name, phone=phone, address=address, postal=postal, price=cost, user=user)
            details.save()
            return redirect('payment')

def payment(request):
    user = request.user
    try:
        global cost
        global person_name
        print(cost)
        user=request.user
        mail = User.objects.filter(username=user).first()
        mail1=mail.email
        response = api.payment_request_create(

            amount=cost,
            purpose='Order Process for your food delivery',
            buyer_name=person_name,
            email=mail1,
            redirect_url='https://127.0.0.1:8000/order_success'
        )
        print(response)


        
        
        print(mail1)
        cart_id = response['payment_request']['id']
        payment= PaymentDetail(payid=cart_id, payuser=person_name, payemail=mail1, payaccount= user)
        payment.save()

        orders = OrderPost.objects.filter(user=user)
        for order in orders:
            order.delete()

        context={"url":response['payment_request']['longurl']}
        return render(request, "foodfest/payment.html", context)
    except Exception as e:
        return HttpResponse("Plese check your connection and make sure you are equipped with proper internet connection and then try again.")

def order_success(request):
    return render(request, "foodfest/order_success.html")

import uuid
def forgotpassword(request):

    if request.method=="POST":
        username=request.POST['name']
        
        
        if User.objects.filter(username=username).first():
            user = User.objects.get(username=username)
            # print(user)
            user_obj=user.email
            # print(user_obj)
            token=str(uuid.uuid4())
            # print(token)
            profile = Profile(user=user)
            profile.forgot_password_token=token
            profile.save()
            send_forgot_password_mail(user_obj,token)
            messages.success(request, "An email has been sent")
            return redirect("/forgotpassword")
            # return render(request, 'foodfest/forgotpassword.html', context)
        else:
            messages.success(request, "User did not exist.")
            return redirect("/forgotpassword")
            # context={"msg":"user does not exist"}
            # return render(request, 'foodfest/forgotpassword.html', context)

    return render(request, "foodfest/forgotpassword.html")

def changepassword(request,token):

    profile = Profile.objects.filter(forgot_password_token=token).first()
    if request.method=="POST":
        new_password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        user_id = request.POST['user_id']

        if user_id is None:
            messages.success(request, "Invalid User.")
            return redirect(f"/changepassword/{token}")

        if new_password!=confirm_password:
            messages.success(request, "Both password must be same.")
            return redirect(f"/changepassword/{token}")

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        messages.success(request, "Your passwpord has been successfully updated. Do login with your new password")
        return redirect('signin')
        
    context = {"user_id":profile.user.id}
    print(profile)

    return render(request, "foodfest/changepassword.html", context)

def signout(request):
    logout(request)
    return redirect('index')