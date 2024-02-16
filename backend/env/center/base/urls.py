from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.home, name="home"),
                  path('about/', views.about, name="about"),
                  path('contact/', views.contact, name="contact"),
                  path('teacher/<int:pk>/', views.teacher, name="teacher"),
                  path('lesson/<int:pk>/', views.lesson, name="lesson"),
                  path('login/', views.login_view, name="login"),
                  path('signup/', views.signup_view, name="signup"),
                  path('logout/', views.logout_view, name="logout"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
