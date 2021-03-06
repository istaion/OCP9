"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('feed/', review.views.feed, name='feed'),
    path('posts/', review.views.posts, name='posts'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('posts/ticket', review.views.ticket_add, name='ticket_add'),
    path('posts/review', review.views.review_add, name='review_add'),
    path('posts/review/<int:ticket_id>/add', review.views.review_response, name='review_response'),
    path('posts/review/<int:review_id>/update', review.views.review_update, name='review_update'),
    path('posts/ticket/<int:ticket_id>/update', review.views.ticket_update, name='ticket_update'),
    path('posts/delete/<int:instance_id>/<str:object_type>', review.views.object_delete, name='delete'),
    path('follow-users/', review.views.follow_users, name='follow_users'),
    path('follow-users/<int:follow_id>/stop-follow', review.views.stop_follow, name='stop_follow')
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
