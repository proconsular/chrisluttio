from django.db import models

class Admin(models.Model):
    password = models.CharField(max_length=255)

class Project(models.Model):
    title = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField()
    work = models.TextField()
    info = models.TextField()
    
class Period(models.Model):
    fromDate = models.DateTimeField()
    toDate = models.DateTimeField()
    project = models.OneToOneField(Project, related_name="period", on_delete=models.CASCADE)

class ListedProject(models.Model):
    order = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    project = models.OneToOneField(Project, related_name="listing", on_delete=models.CASCADE)

class Media(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE)

class Technology(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name="technologies", on_delete=models.CASCADE)
