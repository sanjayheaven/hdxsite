from django.contrib.auth.models import User
from django import forms

from .models import Comment,CommentReply


class CommentForm(forms.ModelForm):
    '''
    '''
    class Meta:
        model = Comment
        fields = ['content']###这里用list方式，或者元祖形式加，号
        # widgets = {
        #     'content': forms.Textarea(attrs={'rows': 5,'placeholder':'评论请使用markdown格式','class':'form-control'}), # 关键是这一行 ###class 放那里?>>>
        # }


class CommentReplyForm(forms.ModelForm):
    '''
    '''
    class Meta:
        model = CommentReply
        fields = ['reply_content','reply_comment','reply']###这里用list方式，或者元祖形式加，号
        # widgets = {
        #     'reply_content': forms.Textarea(attrs={'rows': 5,'placeholder':'评论请使用markdown格式','class':'form-control'}),
        # }
        
