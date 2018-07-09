from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from django.core.files import File
import os
import math

def showIndex(request):
    return render(request, 'main/index.html')

def showProjects(request):
    projects = ListedProject.objects.order_by("order").all()
    grid = []
    for i in range(0, int((len(projects) / 3)) + 1):
        grid.append([])
        for j in range(0, 3):
            if i * 3 + j < len(projects):
                grid[i].append(projects[i * 3 + j])
    context = {
        'grid': grid 
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
        project.role = request.POST['role']
        project.description = request.POST['description']
        project.work = request.POST['work']
        project.info = request.POST['info']
        project.save()
        ListedProject.objects.create(project_id=project.id)

        if len(request.POST['fromDate']) > 0:
            period = Period.objects.create(project_id=project.id, fromDate=request.POST['fromDate'], toDate=request.POST['toDate'])

        if 'video' in request.FILES:
            video = request.FILES['video']
            handle_uploaded_file(project.id, "video", video)
            Media.objects.create(project_id=project.id, name=video.name, type="video", url="global/video/" + str(project.id) + "/" + video.name)

        if 'photo' in request.FILES:
            for file in request.FILES.getlist('photo'):
                handle_uploaded_file(project.id, "images", file)
                Media.objects.create(project_id=project.id, name=file.name, type="image", url="global/images/" + str(project.id) + "/" + file.name)

        if len(request.POST['technologies']) > 0:
            for word in request.POST['technologies'].split(','):
                Technology.objects.create(name=word.strip(), project_id=project.id)

    return redirect(reverse("listed_projects"))

def handle_uploaded_file(project_id, folder, file):
    path = 'media/global/' + folder + '/' + str(project_id) + "/"
    os.makedirs(path, exist_ok=True)
    with open(path + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

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
        project.role = request.POST['role']
        project.description = request.POST['description']
        project.work = request.POST['work']
        project.info = request.POST['info']
        project.save()

        if len(request.POST['fromDate']) > 0:
            if len(Period.objects.filter(project_id=project.id).all()):
                project.period.fromDate = request.POST['fromDate']
                project.period.toDate = request.POST['toDate']
                project.period.save()
            else:
                period = Period.objects.create(project_id=project.id, fromDate=request.POST['fromDate'], toDate=request.POST['toDate'])

        if 'video' in request.FILES:
            for video in request.FILES.getlist('video'):
                handle_uploaded_file(project.id, "video", video)
                Media.objects.create(project_id=project.id, name=video.name, type="video", url="global/video/" + str(project.id) + "/" + video.name)

        if 'photo' in request.FILES:
            for file in request.FILES.getlist('photo'):
                handle_uploaded_file(project.id, "images", file)
                Media.objects.create(project_id=project.id, name=file.name, type="image", url="global/images/" + str(project.id) + "/" + file.name)
        
        if len(request.POST['technologies']) > 0:
            for word in request.POST['technologies'].split(','):
                Technology.objects.create(name=word.strip(), project_id=project.id)
    
    return redirect("/projects/" + request.POST['project'] + "/edit")

def showProject(request, project_id):
    context = {
        'project': Project.objects.get(id=project_id) 
    }
    return render(request, 'main/showProject.html', context)

def showProjectConfirmDelete(request, project_id):
    context = {
        'project': Project.objects.get(id=project_id)
    }
    return render(request, 'main/projectDelete.html', context)

def removeProject(request, project_id):
    project = Project.objects.get(id=project_id)
    for media in project.media.all():
        deleteMedia(media)
    project.listing.delete()
    project.delete()
    return redirect(reverse("listed_projects"))

def deleteMedia(media):
    os.remove("media/" + media.url)
    media.delete()

def removeMedia(request, media_id):
    media = Media.objects.get(id=media_id)
    deleteMedia(media)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteTech(request, tech_id):
    tech = Technology.objects.get(id=tech_id)
    tech.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))