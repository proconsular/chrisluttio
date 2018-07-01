from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *

def showIndex(request):
    return render(request, 'main/index.html')

def showProjects(request):
    context = {
        'projects': ListedProject.objects.order_by("order").all()
    }
    return render(request, 'main/projects.html', context)

def showListedProjects(request):
    context = {
        'projects': ListedProject.objects.order_by("order").all()
    }
    return render(request, 'main/projectList.html', context)

def showProjectForm(request):
    return render(request, 'main/newProject.html')

def createProject(request):
    if (request.method == "POST"):
        project = Project.objects.create()
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.work = request.POST['work']
        project.info = request.POST['info']
        project.save()
        ListedProject.objects.create(project_id=project.id)
    return redirect(reverse("listed_projects"))

def editProjectOrder(request, project_id, direction):
    project = Project.objects.get(id=project_id)
    if direction == "up":
        project.listing.order += -1
    else:
        project.listing.order += 1
    project.listing.save()
    return redirect(reverse("listed_projects"))

def editProjectVisible(request, project_id, visible):
    project = Project.objects.get(id=project_id)
    if visible == "true":
        project.listing.visible = True
    else:
        project.listing.visible = False
    project.listing.save()
    return redirect(reverse("listed_projects"))

def showEditProjectForm(request, project_id):
    context = {
        'project': Project.objects.get(id=project_id)
    }
    return render(request, 'main/editProject.html', context)

def updateProject(request):
    if request.method == "POST":
        project = Project.objects.get(id=request.POST['project'])
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.work = request.POST['work']
        project.info = request.POST['info']
        project.save()
    return redirect(reverse("listed_projects"))
