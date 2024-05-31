from django.urls import path
from .views import token_refresh, token_create


urlpatterns = [
    
    path("token_create/", token_create),
    path("token_refresh/", token_refresh),

]
