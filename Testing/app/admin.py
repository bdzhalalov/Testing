from django.contrib import admin
from .models import Test, Group, Question, Choice


admin.site.register(Group)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['test_name', 'groups']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['text', 'test']


admin.site.register(Question, QuestionAdmin)
