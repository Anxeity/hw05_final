from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Описание тестовой группы',
        )
        cls.post = Post.objects.create(
            author=PostsURLTests.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.aurhorized_client = Client()
        self.aurhorized_client.force_login(PostsURLTests.user)

    def test_home_url_exist(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list_url_exist(self):
        response = self.guest_client.get(f'/group/{PostsURLTests.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_posts_url_exist(self):
        response = self.guest_client.get(f'/posts/{PostsURLTests.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exist(self):
        response = self.guest_client.get('/profile/HasNoName/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page_url_exist(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_edit_post_page_url_exist(self):
        response = self.aurhorized_client.get(
            f'/posts/{PostsURLTests.post.id}/edit/'
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_page_url_exist(self):
        response = self.aurhorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            f'/posts/{PostsURLTests.post.id}/': 'posts/post_detail.html',
            f'/posts/{PostsURLTests.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.aurhorized_client.get(address)
                self.assertTemplateUsed(response, template)
