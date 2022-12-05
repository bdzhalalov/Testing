from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Group, Test


class GroupView(ListView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
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

    def get(self, request, pk):
        test = get_object_or_404(Test, pk=pk)
        context = {
            'test': test
        }
        return render(request, self.template_name, context)
