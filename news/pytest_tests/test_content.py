import pytest

from django.urls import reverse
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, all_news):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, id_for_args, comment_all):
    response = client.get(reverse('news:detail', args=id_for_args))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, id_for_args):
    response = client.get(reverse('news:detail', args=id_for_args))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, id_for_args):
    response = author_client.get(reverse('news:detail', args=id_for_args))
    assert 'form' in response.context
