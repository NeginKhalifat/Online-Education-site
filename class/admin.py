from django.contrib import admin
from .models import Class,Team,Quiz,Question,RecordMark
# Register your models here.

admin.site.register(Class)
admin.site.register(Team)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(RecordMark)
