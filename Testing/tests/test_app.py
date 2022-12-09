import pytest
from django.urls import reverse

from app.models import Choice


@pytest.mark.django_db
def test_groups_url(auto_login_user):
    client, user = auto_login_user()
    url = '/app/groups/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_single_group_url(auto_login_user, group):
    client, user = auto_login_user()
    url = reverse('group_detail', kwargs={'slug': group})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_group_unauthorized(client, group):
    url = reverse('group_detail', kwargs={'slug': group})
    response = client.get(url)

    # redirect to login page
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_test(auto_login_user, test):
    client, user = auto_login_user()
    url = reverse('test_detail', kwargs={'slug': test.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_question(auto_login_user, question, test):
    client, user = auto_login_user()
    url = reverse('question', kwargs={'id': question.pk, 'slug': test.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_choice(question):
    choice1 = Choice.objects.create(choice_text='Value', is_right=False, question=question)
    choice2 = Choice.objects.create(choice_text='Right Value', is_right=True, question=question)
    choice3 = Choice.objects.create(choice_text='Value', is_right=False, question=question)
    assert question.choice_set.all().count() == 3
    assert question.choice_set.filter(is_right=True).count() == 1
