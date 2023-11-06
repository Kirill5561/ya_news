from http import HTTPStatus
import pytest

from django.urls import reverse


"""Тестирование доступности страниц для анонимного пользователя"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('news:home', None),
     ('news:detail', pytest.lazy_fixture('id_for_args')),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = url = reverse(name, args=args)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


"""Тестирование доступности страниц для авторизованного пользователя"""


@pytest.mark.parametrize(
    'name, args',
    (('news:home', None),
     ('news:detail', pytest.lazy_fixture('id_for_args')),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),),
)
def test_pages_availability_for_auth_user(admin_client, name, args):
    url = reverse(name, args=args)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


"""Проверим, что автору заметки доступны страницы отдельной заметки,
её редактирования и удаления."""


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    # Предварительно оборачиваем имена фикстур
    # в вызов функции pytest.lazy_fixture().
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, id_for_args_comment, expected_status
):
    url = reverse(name, args=id_for_args_comment)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
