from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.bookmark_list, name='bookmark_list'),
    path('add/', views.add_bookmark, name='add_bookmark'),
    path('edit/<int:id>/', views.edit_bookmark, name='edit_bookmark'),
    path('delete/<int:id>/', views.delete_bookmark, name='delete_bookmark'),
]
