from pyotp import TOTP
from django.core.mail import send_mail

totp = TOTP('base32secret3232', interval=300)


def generate_otp():
    return totp.now() # returns a number


def send_mail_to_user(user_mail):
    try:
        mail = send_mail(
            subject="OTP Verification for wastebin",
            from_email="idriswisdom6@gmail.com",
            recipient_list=[user_mail],
            message=generate_otp()
        )
    except Exception as e:
        print(e)

