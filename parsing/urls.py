from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name='home'),
    path("tool/<int:tool_id>", views.tools, name='tools'),
    path('', views.articles_list, name='home'),
    path("run_server", views.run_parser),
]
