from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Group, Test, Question, Choice


class GroupView(ListView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        groups = Group.objects.annotate(tests_count=Count('tests__id')).filter(tests_count__gte=1)
        print(groups)
        context = {
            'groups': groups
        }
        return render(request, self.template_name, context)


class GroupViewDetail(ListView):
    template_name = 'groups_detail.html'

    def get(self, request, slug):
        group = Group.objects.get(slug=slug)
        context = {
            'group': group
        }
        return render(request, self.template_name, context)


class TestView(ListView):

    template_name = 'test.html'

    def get(self, request, slug):
        test = get_object_or_404(Test, slug=slug)
        count = Question.objects.select_related().filter(test=test).count()
        context = {
            'test': test,
            'count': count
        }
        return render(request, self.template_name, context)


class QuestionView(ListView):

    template_name = 'question.html'

    def get(self, request, id, slug):
        test = Test.objects.get(slug=slug)
        question = get_object_or_404(Question, pk=id, test=test)
        context = {
            'question': question
        }
        return render(request, self.template_name, context)
