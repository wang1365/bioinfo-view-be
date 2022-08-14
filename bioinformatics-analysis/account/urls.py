from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r"", views.UsersAPIView, "account")


urlpatterns = router.urls
urlpatterns += [
# url(r"^manager", views.UserManagerView.as_view(), name="user_manager"),
    # url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"^validate/$", views.account_validate, name="result"),
]
