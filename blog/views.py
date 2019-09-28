from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View,TemplateView,ListView,DetailView,UpdateView,CreateView
from django.db.models import F,Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.urls import reverse

from .models import Category,Post,Tag
from .forms import SignupForm,LoginForm,AddPostModelForm
from comment.forms import CommentForm,CommentReplyForm

import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# def IndexView(request):
#     # return HttpResponse('<h1>{}<h1>'.format('hello world'))
#     template_name = 'blog/index.html'
#     context = {
#         'name':'hdx',
#     }
#     return render(request,template_name = template_name,context=context)

class AddPostModelFormView(View):
    '''
    创建文章模型表单的View视图，处理get和post两种方法,
    get方法这里整合了修改文章的方式
    '''
    def get(self,request,addpost_id):
        if not addpost_id:
            forms = AddPostModelForm()
            return render(request,'blog/add_post.html',context={'post_forms':forms})
        else:
            post = get_object_or_404(Post,id=addpost_id)
            forms = AddPostModelForm(instance=post)
            return render(request,'blog/add_post.html',context={'post_forms':forms,'delete_update':True})

    def post(self,request,addpost_id):
        if not addpost_id:###这是发表文章入口的判断,区别了发表和(更新,删除),怎么区别更新和删除？？？用button的name和value传值
            forms = AddPostModelForm(request.POST)
        else:
            post = get_object_or_404(Post,id=addpost_id)
            forms = AddPostModelForm(request.POST,instance=post)
        if forms.is_valid():
            post = forms.save(commit=False)
            post.owner = request.user
            if request.POST.get('delete_post',''):
                post.status = Post.STATUS_DELETE
            forms.save()
            if request.POST.get('update_post'):
                return HttpResponseRedirect(reverse('blog:post-detail',kwargs={'post_id':addpost_id}))
            else:
                return HttpResponseRedirect(reverse('blog:index'))

        else:
            return render(request,'blog/add_post.html',context={'post_forms':forms})




class SignupFormView(View):
    '''
    注册表单的View视图，处理get和post两种方法
    '''
    def get(self,request):
        forms = SignupForm()
        return render(request,'blog/signup.html',context={'forms':forms})

    def post(self,request):
        forms = SignupForm(request.POST)###明天看下modelform的参数
        if forms.is_valid():
            if forms.cleaned_data['captcha'] != '978822':
                context = {
                'forms':forms,
                'error': '邀请码错误,请联系博主获取邀请码',
                }
                return render(request,'blog/signup.html',context=context)
            if forms.cleaned_data['re_password'] != forms.cleaned_data['password']:
                context = {
                'forms':forms,
                'error': '两次输入密码不正确,请重新输入密码',
                }
                return render(request,'blog/signup.html',context=context)

            User.objects.create_user(
                username=forms.cleaned_data['username'],
                password=forms.cleaned_data['password'],
                email=forms.cleaned_data['email'],
            ).save()
            return HttpResponseRedirect(reverse('blog:index'))



class LoginFormView(View):
    '''
    登录表单的View视图，处理get和post两种方法
    '''
    def get(self,request):
        forms = LoginForm()
        return render(request,'blog/login.html', context={'forms': forms})

    def post(self,request):
        forms = LoginForm(request.POST)  # 明天看下modelform的参数
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username,password=password)###校验User
            if user and user.is_active:
                login(request,user)###将用户信息保存在session对话中，否则默认为第一访问的状态
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                context = {
                    'forms':forms,
                    'error': '邮箱或者密码错误，请重新输入',
                }
                # locals().update({## locals返回所有的键值
                #     'error':'邮箱或者密码错误，请重新输入'
                # })
                return render(request,'blog/login.html',context=context)

def auth_logout(request):
    logout(request)
    # return render(request,'blog/index.html')###文章显示不出来了
    return HttpResponseRedirect(reverse('blog:index'))


class IndexView(ListView):
    model = Post
    # queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    context_object_name = 'post_list'
    template_name = 'blog/index.html'
    paginate_by = 5##每页显示数量

    # login_url = 'login/'## 登录验证是跳转地址
    # redirect_field_name = ''###等同于next 将next这个键的值送入login_url中去

    extra_context = {
        'forms':SignupForm(),
        'random_tag_colors':['btn-primary','btn-secondary','btn-success','btn-info','btn-warning','btn-danger','btn-light','btn-dark']
    }

    def get_queryset(self):###只展示正常的文章
        queryset = super().get_queryset()
        return queryset.filter(status=Post.STATUS_NORMAL)

    def get_ordering(self):
        order_by = self.request.GET.get('order_by', '')
        self.ordering =  order_by
        return self.ordering

    def get_context_data(self):
        context = super().get_context_data()
        order_by = self.request.GET.get('order_by','')
        context.update({
            'order_by': order_by,
        })
        return context



class PostView(DetailView):
    model = Post ##查看源代码，只要指定model，对象返回模型
    template_name = 'blog/detail.html'
    # context_object_name = 'post'
    pk_url_kwarg = 'post_id'###这里和url那边参数相对应

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.owner:
            obj.update_total_views()
        return obj

    def get_context_data(self,**kwargs):###关键字参数非常重要
        '''
        '''
        pre_posts = Post.objects.filter(id__lt=int(self.kwargs.get(self.pk_url_kwarg))).order_by('-id')
        next_posts = Post.objects.filter(id__gt=int(self.kwargs.get(self.pk_url_kwarg))).order_by('id')
        pre_post = pre_posts[0] if pre_posts else None
        next_post = next_posts[0] if next_posts else None
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_forms':CommentForm(),
            'reply_forms':CommentReplyForm(),
            'pre_post':pre_post,
            'next_post':next_post,
        })
        return context


class CategoryView(IndexView):

    def get_queryset(self):
        '''
        筛选对象
        '''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if not category_id:
            return queryset
        return queryset.filter(category__id=category_id)

    def get_context_data(self):
        '''
        传参
        '''
        context = super().get_context_data()
        context.update({
            'category_id': self.kwargs.get('category_id','')
        })
        return context


class OwnerView(IndexView):
    '''
    用来查找制定作者的文章,利用继承indexviw少些几行代码
    '''
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.kwargs.get('owner_id')
        if not owner_id:
            return queryset
        return queryset.filter(owner__id=owner_id)


class TagView(IndexView):
    '''
    '''

    def get_queryset(self):

        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        if not tag_id:
            return queryset
        return queryset.filter(tag__id=tag_id)

# class TagView(IndexView):
#     '''
#     '''
#     def get_queryset(self):
#         # order_by = self.request.GET.get('order_by', '')
#         # if order_by == 'created_view'
#         queryset = super().get_queryset()
#         tag_id = self.kwargs.get('tag_id')
#         if not tag_id:
#             return queryset
#         return queryset.filter(tag__id=tag_id)



class SearchView(IndexView):

    def get_context_data(self):
        '''
        '''
        context = super().get_context_data()
        context.update({
            'search_keyword': self.request.GET.get('search_keyword', '')
        })
        return context

    def get_queryset(self):
        '''
        '''
        queryset = super().get_queryset()
        print(self.ordering)
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        keyword = self.request.GET.get('search_keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(abstract__icontains=keyword))
