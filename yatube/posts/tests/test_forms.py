from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User, Group, Comment

User = get_user_model()


class FormCreateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы',
        )

        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=self.group
        )

    def test_post_create_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse
                             ('posts:profile',
                              kwargs={'username': 'HasNoName'})
                             )
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост',
            ).exists()
        )

    def test_post_create_form_non_auth(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code,
                         HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_post_edit_form_non_auth(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
        }
        response = self.guest_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response,
                             f'/auth/login/?next=/posts/{self.post.id}/edit/')

        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост',
            ).exists()
        )

    def test_comment_form_non_auth(self):
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), comments_count + 1)

        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий',
            ).exists()
        )