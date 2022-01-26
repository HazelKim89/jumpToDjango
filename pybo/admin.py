from django.contrib import admin
from .models import *


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)