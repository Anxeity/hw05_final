from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Post, Group

User = get_user_model()

INDEX = reverse('posts:index')
PROFILE = reverse('posts:profile', kwargs={'username': 'HasNoName'})


class PaginatorViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы',
        )
        self.authorized_client = Client()
        for i in range(13):
            Post.objects.create(
                author=self.user,
                group=self.group,
            )

    def test_first_page_contains_ten_records(self):
        # Проверка: количество постов на первой странице равно 10.
        response = self.authorized_client.get(INDEX)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        # Проверка: на второй странице должно быть три поста.
        response = self.authorized_client.get(INDEX + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_page_TestGroup_contains_ten_records(self):
        # Проверка: количество постов на первой странице равно 10.
        response = self.authorized_client.get(reverse
                                              ('posts:group_list',
                                               kwargs={
                                                   'slug': self.group.slug}
                                               )
                                              )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_TestGroup_contains_three_records(self):
        # Проверка: количество постов на второй странице равно 3.
        response = self.authorized_client.get(reverse
                                              ('posts:group_list',
                                               kwargs={
                                                   'slug': self.group.slug}
                                               ) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_page_profile_CanEdit_contains_ten_records(self):
        response = self.authorized_client.get(PROFILE)
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_profile_CanEdit_contains_three_records(self):
        # Проверка: количество постов на второй странице равно 3.
        response = self.authorized_client.get(PROFILE + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
