"""hdxsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # path('', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('signup/',views.SignupFormView.as_view(),name='signup'),
    path('login/',views.LoginFormView.as_view(),name='login'),
    path('logout', views.auth_logout, name='auth_logout'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('post/<int:post_id>/',views.PostView.as_view(),name='post-detail'),###文章详情页
    path('add_post/<int:addpost_id>/',views.AddPostModelFormView.as_view(),name='post-add'),###文章详情页
    

    path('tag/<int:tag_id>/',views.TagView.as_view(),name='tag-list'),##展示这个标签下的所有文章 ，还是以card样式展示，所以继承indexview，只是过滤post对象
    path('category/<int:category_id>/',views.CategoryView.as_view(),name='category-list'),##展示这个分类下的所有文章 ，还是以card样式展示
    path('owner/<int:owner_id>/',views.OwnerView.as_view(),name='owner-list'),##展示这个作者下的所有文章 ，还是以card样式展示

]
