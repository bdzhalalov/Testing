# Import from third-party libraries
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Import from current project
from .models import Group, Test, Question, Choice, Answer, Attempt


class GroupView(LoginRequiredMixin, ListView):
    template_name = 'main.html'

    # Get a list of test groups
    def get(self, request, *args, **kwargs):
        groups = Group.objects.annotate(tests_count=Count('tests__id')).filter(tests_count__gte=1)
        context = {
            'groups': groups
        }
        return render(request, self.template_name, context)


class GroupViewDetail(LoginRequiredMixin, ListView):
    template_name = 'groups_detail.html'

    # Get a test group
    def get(self, request, slug):
        group = get_object_or_404(Group, slug=slug)
        context = {
            'group': group
        }
        return render(request, self.template_name, context)


class TestView(LoginRequiredMixin, ListView):

    template_name = 'test.html'

    # Get a single test from test group
    def get(self, request, slug):
        test = get_object_or_404(Test, slug=slug)

        # Variable for displaying questions count in test
        count = test.question_set.all().count()

        context = {
            'test': test,
            'count': count
        }
        return render(request, self.template_name, context)


class QuestionView(LoginRequiredMixin, ListView):

    template_name = 'question.html'

    def get(self, request, id, slug):

        # Get objects for displaying
        test = Test.objects.get(slug=slug)
        question = get_object_or_404(Question, pk=id, test=test)

        # These variables need for correct submit buttons displaying
        questions_count = test.question_set.all().count()
        last_id = test.question_set.all()[questions_count - 1].id

        # choice context for submit buttons
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

        # Get objects needed for further operations
        test = Test.objects.get(slug=slug)
        question = get_object_or_404(Question, pk=id, test=test)
        attempt = Attempt.objects.filter(user=request.user, test=test).count()

        # Take data from form
        choice = request.POST.getlist('choice')

        # Create an Answer object using data from form and certain variables
        for elements in choice:
            choice_value = Choice.objects.get(pk=elements)
            Answer.objects.create(
                user=request.user, test=test, question=question, choice=choice_value, attempt=attempt+1
            )

        # Variables for correct function returning
        questions_count = test.question_set.all().count()
        last_id = test.question_set.all()[questions_count - 1].id

        # choice function returning
        if id == last_id:
            # create attempt for split answers based on number of attempt and redirect to result page
            Attempt.objects.create(user=request.user, test=test)
            return redirect(reverse('result', kwargs={'slug': slug}))

        # if id != last_id
        return redirect(question.get_next_question())


def get_result(request, slug):

    # Get objects needed for further operations
    user = request.user
    test = Test.objects.get(slug=slug)
    question = Question.objects.filter(test=test)
    attempt = test.attempt_set.filter(user=user, test=test).count()

    right_questions = 0

    # Get user answers for test questions
    for que in question:
        answer = Answer.objects.filter(user=user, test=test, question=que, attempt=attempt)

        # count of right user answers for question
        count = 0
        for el in answer:
            if el.choice.is_right:
                count += 1

        # checking variables for correct counter work
        if que.choice_set.filter(is_right=True).count() == count == answer.count():
            right_questions += 1

    # get percent of correct answers
    percent = round((right_questions / question.count()) * 100)

    # make a context for template
    context = {
        'test': test,
        'user': user,
        'question': question,
        'right_questions': right_questions,
        'percent': percent
    }
    return render(request, 'result.html', context)

# TODO: make general statistics on passed tests by user
