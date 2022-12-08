from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Group, Test, Question, Choice, Answer, Attempt


class GroupView(ListView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        groups = Group.objects.annotate(tests_count=Count('tests__id')).filter(tests_count__gte=1)
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

        questions_count = test.question_set.all().count()
        last_id = test.question_set.all()[questions_count - 1].id
        if id == last_id:
            context = {
                'question': question,
                'finish': 'true'
            }
        else:
            context = {
                'question': question,
                'next': id + 1
            }
        return render(request, self.template_name, context)

    def post(self, request, id, slug):
        test = Test.objects.get(slug=slug)
        question = get_object_or_404(Question, pk=id, test=test)
        attempt = Attempt.objects.filter(user=request.user, test=test).count()

        choice = request.POST.getlist('choice')

        for elements in choice:
            choice_value = Choice.objects.get(pk=elements)
            Answer.objects.create(user=request.user, test=test, question=question, choice=choice_value, attempt=attempt+1)

        questions_count = test.question_set.all().count()
        last_id = test.question_set.all()[questions_count - 1].id

        if id == last_id:
            Attempt.objects.create(user=request.user, test=test)
            return redirect(reverse('result', kwargs={'slug': slug}))
        return redirect(question.get_next_question())


def get_result(request, slug):
    user = request.user
    test = Test.objects.get(slug=slug)
    question = Question.objects.filter(test=test)
    attempt = test.attempt_set.filter(user=user, test=test).count()
    right_questions = 0
    for que in question:
        answer = Answer.objects.filter(user=user, test=test, question=que, attempt=attempt)
        count = 0
        for el in answer:
            if el.choice.is_right:
                count += 1

        if que.choice_set.filter(is_right=True).count() == count == answer.count():
            right_questions += 1

    percent = round((right_questions / question.count()) * 100)
    context = {
        'test': test,
        'user': user,
        'question': question,
        'right_questions': right_questions,
        'percent': percent
    }
    return render(request, 'result.html', context)
