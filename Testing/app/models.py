from django.conf import settings
from django.db import models
from django.urls import reverse


class Test(models.Model):
    test_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, null=True)
    groups = models.ManyToManyField('Group', blank=True, related_name='tests')

    def __str__(self):
        return self.test_name

    def get_url(self):
        return reverse('test_detail', kwargs={'slug': self.slug})


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)

    def __str__(self):
        return f'Вопрос: {self.text}'

    def get_url(self):
        return reverse('question', kwargs={'id': self.pk, 'slug': self.test.slug})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Group(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('group_detail', kwargs={'slug': self.slug})


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.choice.choice_text
