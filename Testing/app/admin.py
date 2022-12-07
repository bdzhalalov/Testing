from django.contrib import admin
from .models import Test, Group, Question, Choice, Answer


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Group, GroupAdmin)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class TestAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('test_name',)
    }
    fieldsets = [
        (None, {'fields': ['test_name', 'slug', 'groups']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text', 'test']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['text', 'test']
    list_filter = ['test', 'text']
    search_fields = ['test__test_name', 'text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)