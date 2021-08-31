from django.db import models

from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify


class Team(models.Model):
    name = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    members = models.ManyToManyField(User, related_name='members')
    slug = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Class.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse('class:class_list', kwargs={'slug': self.slug})


def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance._get_unique_slug()


pre_save.connect(rl_pre_save_reciever, sender=Team)


class ClassQueryset(models.query.QuerySet):
    def search(self, query):
        return self.filter(
            Q(title_icontains=query) |
            Q(owner_username__icontains=query)
        ).distinct()


class ClassManager(models.Manager):
    def get_queryset(self):
        return ClassQueryset(self.model, using=self.db)

    def search(self, query):
        return self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(owner__username__icontains=query)
        ).distinct()


class Class(models.Model):
    title = models.CharField(max_length=30)
    teams = models.ManyToManyField('Team', related_name='teams')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    description = models.CharField(max_length=90, blank=True)
    duration = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    objects = ClassManager()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Class.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('class:class_list', kwargs={'slug': self.slug})


pre_save.connect(rl_pre_save_reciever, sender=Class)


class Quiz(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    date = models.CharField(max_length=30)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Class.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def __str__(self):
        return self.name


class Question(models.Model):
    questions = models.CharField(max_length=200,null=True)
    option1 = models.CharField(max_length=90, default="")
    option2 = models.CharField(max_length=90, default="")
    option3 = models.CharField(max_length=90, default="")
    option4 = models.CharField(max_length=90, default="")
    answer = models.CharField(max_length=90, default="")
    exam = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    value = models.FloatField(null=True)


pre_save.connect(rl_pre_save_reciever, sender=Quiz)


class RecordMark(models.Model):
    participants = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=False, auto_now_add=True)
    mark = models.FloatField(blank=True)
