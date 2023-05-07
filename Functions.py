import smtplib
import ssl
from email.message import EmailMessage
import random
import string

def twostepcheck(receiver):
    email_sender= "dvibeslildeep@gmail.com"
    email_password ="ehvjllblgpjttanm"
    email_receiver = receiver
    subject ="Account Confirmation Code for DVibes"
    code = get_random_string(8)
    body= """\nDear Explorer,\n
    Thank you for creating an account with DVibes. To confirm your account, please enter the following confirmation code:\n\n
    {}\n\n
    If you did not create an account with DVibes, please disregard this email.\n\n
    Thank you for choosing DVibes and we look forward to serving you.\n\n
    Best regards,\n
    Omar Kateb\n
    DVibes Team\n
    """.format(code)
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

def Coach_password(receiver):
    email_sender= "dvibeslildeep@gmail.com"
    email_password ="ehvjllblgpjttanm"
    email_receiver = receiver
    subject ="Your Request to Become a Coach on DVibes Has Been Approved!"
    code = get_random_string(8)
    body= """Dear Coach,\n\n
    We are excited to inform you that your request to become a coach at Dvibes has been accepted by our team.
    We appreciate your interest in joining our community of coaches and we are confident that you will contribute
    to our mission of helping individuals achieve their goals.\n\n
    As part of the registration process, we are sending you your password for your Dvibes account:\n\n
    Password: {}\n\n
    Please note that this password is case-sensitive and should be kept confidential.
    We recommend that you change your password upon logging in for the first time.\n\n
    We look forward to seeing your profile and coaching services on our platform.\n\n
    Best regards,\n
    # The Dvibes Team\n
    """.format(code)
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
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    all_characters = lowercase + uppercase + numbers
    shuffled_characters = random.sample(all_characters, len(all_characters))
    result_str = ''.join(random.choices(shuffled_characters, k=length))
    return result_str