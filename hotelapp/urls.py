from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('profile/',views.profile,name='profile'),
    path('login',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<uid>', views.delete, name='delete'),
    path('register/',views.register_view,name='register'),
    path('rooms/<uid>/',views.rooms,name='room'),
    path('adminpage',views.adminpage,name='admin'),
    path('admin/',views.adminpage,name='admins'),
    path('payment',views.payment,name='payment'),
    
]
