from captcha.fields import CaptchaField
from django import forms

class RegisterForm(forms.Form):
    captcha = CaptchaField(error_messages={'invalid': '验证码输入有误'})
    # captcha = CaptchaField()