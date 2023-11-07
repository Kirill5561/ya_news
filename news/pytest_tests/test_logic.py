import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

NEW_COMMENT_TEXT = 'Новый текст'


@pytest.mark.django_db
def test_user_can_create_note(news, id_for_args, author_client, author,
                              form_data):
    url = reverse('news:detail', args=id_for_args)
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    new_note = Comment.objects.get()
    assert new_note.text == form_data['text']
    assert new_note.author == author
    assert new_note.news == news


@pytest.mark.django_db
def test_user_cant_use_bad_words(id_for_args, author_client):
    url = reverse('news:detail', args=id_for_args)
    bad_text = {'text': f'Текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_text)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client,
                                   id_for_args,
                                   id_for_args_comment):
    url = reverse('news:delete', args=id_for_args_comment)
    url_to_comments = reverse('news:detail', args=id_for_args) + '#comments'
    response = author_client.delete(url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client,
                                                  id_for_args_comment):
    url = reverse('news:delete', args=id_for_args_comment)
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client,
                                 id_for_args,
                                 id_for_args_comment,
                                 form_data, comment):
    edit_url = reverse('news:edit', args=id_for_args_comment)
    url_to_comments = reverse('news:detail', args=id_for_args) + '#comments'
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(admin_client,
                                                id_for_args_comment, form_data,
                                                comment):
    edit_url = reverse('news:edit', args=id_for_args_comment)
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != NEW_COMMENT_TEXT
