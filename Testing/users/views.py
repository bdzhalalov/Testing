from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm


class Registration(CreateView):
    template_name = 'registration/register.html'

    # get registration form
    def get(self, request, *args, **kwargs):
        context = {
            'form': RegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST)

        # check form validity
        if form.is_valid():
            form.save()

            # autologin on service after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('main')

        # if form not valid
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
