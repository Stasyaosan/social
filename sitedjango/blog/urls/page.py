from django.urls import path
from blog.views import *

main_patterns = [
    path('articles/', articles),
    path('', index),
]