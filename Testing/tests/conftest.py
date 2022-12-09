import pytest
from django.test import Client
from app.models import Test, Question, Group


@pytest.fixture
def test_password():
    return 'test_password'


@pytest.fixture
def create_user(client, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'Test_user'
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user
    return make_auto_login


@pytest.fixture
def group():
    group = Group.objects.create(title='python', slug='python')
    return group


@pytest.fixture
def test(group):
    test = Test.objects.create(test_name='Test', slug='test')
    test.groups.add(group)
    return test


@pytest.fixture
def question(test):
    question = Question.objects.create(text='Test question', test=test)
    return question
