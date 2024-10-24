from django.contrib import admin
from django.urls import path
from .views import Index , SignupView, Dashboard, AddItem, EditItem, DeleteItem, SellItem
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('sell/<int:item_id>/', SellItem.as_view(), name='sell-item'),
]
