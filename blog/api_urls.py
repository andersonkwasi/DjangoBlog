from django.urls import path
from blog.views import ArticleApi

urlpatterns = [
    path('', ArticleApi)
]