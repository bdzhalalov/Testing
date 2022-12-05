from django.shortcuts import render
from django.views.generic import ListView

from .models import Group


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
