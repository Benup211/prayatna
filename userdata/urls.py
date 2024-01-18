from django.urls import path
from .views import RegisterView,LoginView,LogoutView,HomeView,AddCardView
app_name='userdata'
urlpatterns=[
    path('',HomeView.as_view(),name='home'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('addcard/',AddCardView.as_view(),name='addcard'),
]