import pytest

from django.urls import reverse
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, all_news):
    # Загружаем главную страницу.
    response = client.get(reverse('news:home'))
    # Код ответа не проверяем, его уже проверили в тестах маршрутов.
    # Получаем список объектов из словаря контекста.
    object_list = response.context['object_list']
    # Определяем длину списка.
    news_count = len(object_list)
    # Проверяем, что на странице именно 10 новостей.
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    # Получаем даты новостей в том порядке, как они выведены на странице.
    all_dates = [news.date for news in object_list]
    # Сортируем полученный список по убыванию.
    sorted_dates = sorted(all_dates, reverse=True)
    # Проверяем, что исходный список был отсортирован правильно.
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, id_for_args, comment_all):
    response = client.get(reverse('news:detail', args=id_for_args))
    # Проверяем, что объект новости находится в словаре контекста
    # под ожидаемым именем - названием модели.
    assert 'news' in response.context
    # Получаем объект новости.
    news = response.context['news']
    # Получаем все комментарии к новости.
    all_comments = news.comment_set.all()
    # Проверяем, что время создания первого комментария в списке
    # меньше, чем время создания второго.
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, id_for_args):
    response = client.get(reverse('news:detail', args=id_for_args))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, id_for_args):
    response = author_client.get(reverse('news:detail', args=id_for_args))
    assert 'form' in response.context
