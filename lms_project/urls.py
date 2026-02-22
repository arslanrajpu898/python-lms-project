from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's Login tools
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/complete/', views.mark_complete, name='mark_complete'),
    path('chatbot/', views.chatbot_api, name='chatbot'),

    # --- Authentication URLs ---
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]