from django.contrib.auth.models import User
# from django.db.models import
from django import forms
from .models import Post
from comment.models import CommentReply



class SignupForm(forms.Form):
    '''
    '''
    username = forms.CharField(min_length=3, max_length=150, label='用户/手机/邮箱', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=6,max_length=150,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    re_password = forms.CharField(min_length=6,max_length=150,label='确认密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = forms.CharField(min_length=3, max_length=150,label='输入邀请码', widget=forms.TextInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    '''
    '''
    username = forms.CharField(min_length=3, max_length=150, label='用户/手机/邮箱', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=3,max_length=150,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class AddPostModelForm(forms.ModelForm):
    '''
    '''
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['total_views', 'update_time', 'status']
        widgets = {
            'title':
            forms.TextInput(attrs={'class': 'form-control'}),
            'abstract':
            forms.TextInput(attrs={
                'class': 'form-control',
            }),
            # 'content':
            # forms.Textarea(attrs={
            #     'class': 'form-control',
            #     'placeholder': '请使用markdown语法编辑文章'
            # }),
            'category':
            forms.Select(attrs={'class': 'form-control'}),
            'tag':
            forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
