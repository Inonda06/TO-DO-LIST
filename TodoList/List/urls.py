from typing import List
from django.urls import path
from .views import CustomLoginView,TaskView,TaskDetailView,TaskCreateView, TaskUpdateView, TaskDeleteView, RegisterPageView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/",CustomLoginView.as_view(), name='login'),
    path("logOut/",LogoutView.as_view(next_page='login'), name='logout'),
    path("",TaskView.as_view(), name='tasks'),
    path("Register/", RegisterPageView.as_view(), name='register'),
    path("Create/",TaskCreateView.as_view(), name= 'create'),
    path("Details/<str:pk>/",TaskDetailView.as_view(), name= 'details'),
    path("Update/<str:pk>/",TaskUpdateView.as_view(), name= 'Update'),
    path("delete/<str:pk>/",TaskDeleteView.as_view(), name= 'delete'),
]