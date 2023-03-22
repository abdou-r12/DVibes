import smtplib
import ssl
from email.message import EmailMessage
import random
import string

def twostepcheck(receiver):
    email_sender= "abdoupolo29@gmail.com"
    email_password ="oxbcpxmjwubxufox"
    email_receiver = receiver
    subject ="Confirmation code"
    code = get_random_string(8)
    body= "Your code is " + code
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    return code

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str