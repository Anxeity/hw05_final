from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from ..models import Post, Group, Comment


User = get_user_model()


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.user2 = User.objects.create_user(username='HasName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(PostViewsTests.user)
        cls.guest_client = Client()

    def setUp(self):
        # Создаем авторизованный клиент
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы',
        )

        self.user = User.objects.get(username='HasNoName')

        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=self.group,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            text='Тестовый комментарий',
            author=self.user,
        )

        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewsTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(PostViewsTests.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}
                    ): 'posts/group_list.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}
                    ): 'posts/create_post.html',
            reverse('posts:profile',
                    kwargs={'username': 'HasNoName'}
                    ): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}
                    ): 'posts/post_detail.html',
            reverse('posts:post_create'
                    ): 'posts/create_post.html',

        }
        # Проверяем, что при обращении вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Точка Невозврата
    def test_index_shows_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        test_object = response.context.get('page_obj')[0]
        self.assertEqual(test_object, self.post)

    def test_group_list_shows_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        test_object = response.context['page_obj'][0]
        test_group = response.context['group']
        self.assertEqual(test_object, self.post)
        self.assertEqual(test_group, self.group)

    def test_profile_shows_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        test_object = response.context.get('page_obj')[0]
        test_author = response.context['author']
        self.assertEqual(test_object, self.post)
        self.assertEqual(test_author, self.post.author)

    def test_post_detail_shows_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        test_post = response.context['post']
        test_post_count = response.context['post_count']
        self.assertEqual(test_post, self.post)
        self.assertEqual(test_post_count, self.post.author.posts.count())

    def test_edit_post_shows_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': '1'})
        )
        test_is_edit = response.context['is_edit']
        form_fields = {
            'text': forms.fields.CharField,
        }
        form_field = response.context.get('form').fields.get('text')
        self.assertIsInstance(form_field, form_fields['text'])
        self.assertTrue(test_is_edit)

    def test_post_create_shows_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_create'))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.MultipleChoiceField,
        }
        form_field = response.context.get('form').fields.get('text')
        self.assertIsInstance(form_field, form_fields['text'])

    def test_new_post_index(self):
        response = self.authorized_client.get(reverse('posts:index'))
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый пост')
        self.assertIn(post, posts)

    def test_new_post_group(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый пост')
        self.assertIn(post, posts)

    def test_new_post_profile(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'HasNoName'})
        )
        posts = response.context.get('page_obj').object_list
        post = Post.objects.get(text='Тестовый пост')
        self.assertIn(post, posts)

    def test_cache_index(self):
        response = self.authorized_client.get(
            reverse('posts:index')
        )
        resp_1 = response.content
        post_deleted = Post.objects.get(id=1)
        post_deleted.delete()
        response_anoth = self.authorized_client.get(
            reverse('posts:index')
        )
        resp_2 = response_anoth.content
        self.assertTrue(resp_1 == resp_2)
