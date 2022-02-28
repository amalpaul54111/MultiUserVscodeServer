from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "vscode"   


urlpatterns = [
    path("", views.homepage, name="main"),
    path("login",views.user_login,name="login"),
    path("logout",views.user_logout,name="logout"),
    path("register", views.register_request, name="register")
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)