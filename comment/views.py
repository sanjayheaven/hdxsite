from django.shortcuts import render,get_object_or_404,redirect
# from django.urls import

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views.generic import View,DetailView,ListView,DeleteView,UpdateView,CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CommentForm,CommentReplyForm

from blog.models import Post
from .models import Comment,CommentReply
# import requests


from notifications.signals import notify

# notify.send(actor, recipient, verb, target, action_object)



class NotificationView(View):

    def get(self,request):
        un_read_item_id = request.GET.get('un_read_item_id')
        un_read_item_target_id = request.GET.get('un_read_item_target_id')
        un_read_item_action_object = request.GET.get('un_read_item_action_object')
        un_read_item_action_object_id = request.GET.get('un_read_item_action_object_id')
        if not un_read_item_id or not un_read_item_target_id or not un_read_item_action_object or not un_read_item_action_object_id:
            request.user.notifications.mark_all_as_read()
            # print(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            request.user.notifications.get(id=int(un_read_item_id)).mark_as_read()
            redirect_url = reverse('blog:post-detail',kwargs={'post_id':un_read_item_target_id}) + '#'+un_read_item_action_object+'_'+un_read_item_action_object_id
            print(redirect_url)
            return HttpResponseRedirect(redirect_url)




class CommentFormView(View):

    def post(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        comment_forms = CommentForm(request.POST)
        if comment_forms.is_valid():
            comment = comment_forms.save(commit=False)
            comment.owner = request.user
            comment.post = post
            comment.save()
            # if not post.user.is_superuser:
            notify.send(
                request.user,
                recipient=post.owner,
                verb='评论了你',
                target=post,
                description=comment.content,
                action_object=comment
            )
            redirect_url = reverse('blog:post-detail',kwargs={'post_id':post_id}) + '#comment_area'
            return HttpResponseRedirect(redirect_url)


class CommentReplyFormView(View):

    def post(self,request,post_id):
        # print('(############)')
        # print(self.kwargs)
        # print('(############)')
        # print(request.GET)
        reply_comment_id = request.POST.get('reply_comment_id')
        reply_id = request.POST.get('reply_id')

        comment = get_object_or_404(Comment, id=int(reply_comment_id))
        if reply_id :
            reply = get_object_or_404(CommentReply, id=int(reply_id))

        reply_forms = CommentReplyForm(request.POST)

        if reply_forms.is_valid():
            reply_tmp = reply_forms.save(commit=False)
            reply_tmp.owner = request.user
            reply_tmp.reply_comment = comment
            if reply_id :
                reply_tmp.reply = reply
            reply_tmp.save()
            notify.send(
                request.user,
                recipient=comment.post.owner,
                verb='回复了你',
                target=comment.post,
                description=reply_tmp.reply_content,
                action_object=reply_tmp,
            )
            redirect_url = reverse('blog:post-detail',kwargs={'post_id':post_id}) + '#comment_area'
            return HttpResponseRedirect(redirect_url)
