from datetime import timedelta 
from django.utils import timezone
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class Utlil:
    @staticmethod
    def send_email(data):
        email_body = render_to_string('email_template.html', {'username': data['username'], 'code': data['code']})
        email = EmailMessage(subject=data['email_subject'], body=email_body, to=[data['to_email']])
        email.content_subtype = 'html'
        email.send()



def get_expiration_time():
    return timezone.now() + timedelta(minutes=10)



def generate_code():
    code_verivecation = random.randint(1000,9999)
    return code_verivecation
