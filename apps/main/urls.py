from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.showIndex, name="index"),
    path('projects', views.showProjects, name="projects"),
    path('projects/listed', views.showListedProjects, name="listed_projects"),
    path('projects/new', views.showProjectForm),
    path('projects/create', views.createProject, name="createProject"),
    url(r'^projects/(\d+)/edit/order/([a-z]+)$', views.editProjectOrder),
    url(r'^projects/(\d+)/edit/visible/([a-z]+)$', views.editProjectVisible),
    url(r'^projects/(\d+)/edit$', views.showEditProjectForm),
    path('projects/update', views.updateProject, name="updateProject"),
]
