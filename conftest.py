import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from news.models import News, Comment


""" Пользователи """


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


""" Новости """


@pytest.fixture
def all_news():
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}',
                    text='Просто текст.',
                    date=datetime.today() - timedelta(days=index))
        all_news.append(news)
    News.objects.bulk_create(all_news)


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def id_for_args(news):
    return news.id,


""" Коментарии """


@pytest.fixture
def comment_all(author, news):
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария{index}',)
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def id_for_args_comment(comment):
    return comment.id,


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }
