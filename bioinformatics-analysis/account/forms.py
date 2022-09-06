from django import forms
import re
from django.forms import widgets

from account.models import Account

# class LoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget = widgets.TextInput(
#             attrs={'placeholder': "username", "class": "form-control"})
#         self.fields['password'].widget = widgets.PasswordInput(
#             attrs={'placeholder': "password", "class": "form-control"})


# class RegisterForm(UserCreationForm):
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise ValidationError("该邮箱已经存在.")
#         return email
#
#     class Meta:
#         model = get_user_model()
#         fields = ("username", "email")


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=30,
        min_length=1,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入用户名"}
        ),
    )
    nickname = forms.CharField(
        label="姓名",
        max_length=30,
        min_length=1,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入姓名"}
        ),
    )
    email = forms.EmailField(
        required=False,
        label="邮箱",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "请输入邮箱"}
        ),
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请输入密码"}
        ),
    )
    password_again = forms.CharField(
        label="再次输入密码",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请再次输入密码"}
        ),
    )

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop("request")
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在, 请修改用户名")
        return username

    def clean_nickname(self):
        return self.cleaned_data["nickname"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and not email.endswith("nanodigmbio.com"):
            raise forms.ValidationError("邮箱后缀名必须是nanodigmbio.com")
        if email and Account.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("两次密码输入不一致")
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data["verification_code"].strip()
        if verification_code == "":
            raise forms.ValidationError("验证码不能为空")

        # 判断验证码
        code = self.request.session.get("register_code", "")
        verification_code = self.cleaned_data.get("verification_code", "")
        if not (code != "" and code == verification_code):
            raise forms.ValidationError("验证码错误")
        return verification_code


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=widgets.TextInput(
            attrs={
                "class": "form-control",
                "name": "username",
                "id": "username",
                "placeholder": "请输入用户名",
                "autofocus": "autofocus",
            }
        )
    )
    password = forms.CharField(
        widget=widgets.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password",
                "id": "password",
                "placeholder": "请输入密码",
            }
        )
    )
