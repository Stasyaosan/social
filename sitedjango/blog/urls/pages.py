from django.urls import path
from blog.views import *

main_patterns = [
    path('articles/', articles),
    path('', index),
    path('article/<int:id>', articlesid),
    path('addarticle/', addarticle),
    path('snake/', snake, name='snake'),
]

user_patterns = [
    path('reg/', reg),
    path('auth/', auth),
    path('user/panel/', panel),
    path('user/mystory/', mystory),
    path('logout/', logout),
    path('users/', users),
    path('listarticles/', listarticles),
    path('users/<str:login>', userdetail),
    path('addfriend/', addfriend),
    path('addavatar/', addavatar),
]

chat_patterns = [
    path('chat/<int:id>', chatid),
    path('ajaxchat/', ajaxchat),
    path('ajaxdelete/', ajaxdelete),
]

contacts_patterns = [
    path('contacts/', contacts),
    path('contact/', contact),
]