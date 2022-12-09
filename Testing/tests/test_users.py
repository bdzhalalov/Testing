import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register(create_user, test_password, client):
    url = '/users/registration/'
    user = create_user()
    response = client.post(url, dict={'username': user, 'password': test_password})
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(auto_login_user):
    client, user = auto_login_user()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
