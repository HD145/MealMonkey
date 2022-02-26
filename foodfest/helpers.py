from email import message
from django.core.mail import send_mail
from django.conf import settings

def send_forgot_password_mail(email,token):

    subject = "Your fogot password link"
    message = f'Hi,click on the link to reset your password http://127.0.0.1:8000/changepassword/{token} '
    # message="HELLO FROM WORKWITHUS"
    email_from = settings.EMAIL_HOST_USER
    # print(email_from)
    recipient_list = [email]
    # print(recipient_list)
    send_mail(subject,message,email_from,recipient_list, fail_silently=False)
    return True