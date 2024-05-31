from django.urls import path
from .views import get_all_teachers,  get_all_classes, add_balls, get_class, remove_balls, start, get_quater_balls


urlpatterns = [
    path("teachers/", get_all_teachers),
    path("classes/", get_all_classes),
    path("add_balls/", add_balls),
    path("get_class/", get_class),
    path("remove_balls/", remove_balls),
    path("get_qb/", get_quater_balls),
    path("start/", start)
]