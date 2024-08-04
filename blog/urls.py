from django.urls import path
from blog.views import blogHomeView, BlogCreateView, BlogUpdateView,BlogDeleteView,BlogDetailView

app_name = "blog"

urlpatterns = [
    path('', blogHomeView.as_view(), name='home'),
    path('add/', BlogCreateView.as_view(), name="ajout"),
    path('edit/<str:slug>/', BlogUpdateView.as_view(), name="modifier"),
    path('delete/<str:slug>/', BlogDeleteView.as_view(), name='suppression'),
    path('detail/<str:slug>/',BlogDetailView.as_view(), name="detail")
]