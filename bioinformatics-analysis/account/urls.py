from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.UsersAPIView.as_view()),
    url(r"^manager", views.UserManagerView.as_view(), name="user_manager"),
    # url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"^validate/$", views.account_validate, name="result"),
]
