#自定义图文验证码表单
#一般将一些表单类写到同一个forms.py文件里
from captcha.fields import CaptchaField
from django import forms
class RegisterForm(forms.Form):
    #为生成的验证码图片，以及输入框.
    captcha = CaptchaField()