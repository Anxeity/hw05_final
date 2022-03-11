from django.test import TestCase, Client

from ..models import Post, Group, User


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
        self.urls = {
            "homepage": '/',
            "group_page": '/group/test_slug/',
            "profile_page": '/profile/HasNoName/',
            "post_view_page": f'/posts/{PostsURLTests.post.id}/',
            "post_edit_page": f'/posts/{PostsURLTests.post.id}/edit/',
            "post_create": '/create/',
            "not_found_page": "/fjgjsg/",
        }

    def test_home_url_exist(self):
        response = self.guest_client.get(self.urls["homepage"])
        self.assertEqual(response.status_code, 200)

    def test_group_list_url_exist(self):
        response = self.guest_client.get(self.urls["group_page"])
        self.assertEqual(response.status_code, 200)

    def test_posts_url_exist(self):
        response = self.guest_client.get(self.urls["post_view_page"])
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exist(self):
        response = self.guest_client.get(self.urls["profile_page"])
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page_url_exist(self):
        response = self.guest_client.get(self.urls["not_found_page"])
        self.assertEqual(response.status_code, 404)

    def test_edit_post_page_url_exist(self):
        response = self.aurhorized_client.get(
            self.urls["post_edit_page"]
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_page_url_exist(self):
        response = self.aurhorized_client.get(self.urls["post_create"])
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            self.urls["homepage"]: 'posts/index.html',
            self.urls["group_page"]: 'posts/group_list.html',
            self.urls["profile_page"]: 'posts/profile.html',
            self.urls["post_view_page"]: 'posts/post_detail.html',
            self.urls["post_edit_page"]: 'posts/create_post.html',
            self.urls["post_create"]: 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.aurhorized_client.get(address)
                self.assertTemplateUsed(response, template)
