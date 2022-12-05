from django.db import models
from django.urls import reverse


class Test(models.Model):
    test_name = models.CharField(max_length=64)
    groups = models.ManyToManyField('Group', blank=True, related_name='tests')

    def __str__(self):
        return self.test_name

    def get_url(self):
        return reverse('test_detail', kwargs={'pk': self.id})


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)

    def __str__(self):
        return self.text


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
