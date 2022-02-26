from unicodedata import name
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('orderpost/<id>', views.orderpost, name="orderpost"),
    path('deleteorder/<order_id>', views.deleteorder, name="deleteorder"),
    path('vieworder/<id>', views.vieworder, name="vieworder"),
    path('yourorders', views.yourorders, name="yourorders"),
    path('search', views.search, name="search"),
    path('person_details', views.person_details, name="person_details"),
    path('payment', views.payment, name="payment"),
    path('order_success', views.order_success, name="order_success"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('changepassword/<token>', views.changepassword, name="changepassword"),
]
