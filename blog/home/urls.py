from django.urls import path
from .views import BlogView,PublicView

urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('',PublicView.as_view())
]
