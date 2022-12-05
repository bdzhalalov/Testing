from django.contrib import admin
from .models import Test, Group, Question, Choice


admin.site.register(Test)
admin.site.register(Group)
admin.site.register(Question)
admin.site.register(Choice)
