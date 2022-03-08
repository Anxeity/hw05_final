from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow

User = get_user_model()


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(
            username='Stanislav'
        )
        cls.follower = User.objects.create(
            username='Kotovskiy'
        )

    def test_add_follow(self):
        self.assertEqual(Follow.objects.count(), 0)
        client_follower = Client()
        client_follower.force_login(FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_follow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 1)
        follow = Follow.objects.first()
        self.assertEqual(follow.author, FollowTest.author)
        self.assertEqual(follow.user, FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_follow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 1)
        follows = Follow.objects.filter(
            author=FollowTest.author,
            user=FollowTest.follower)
        self.assertEqual(len(follows), 1)

    def test_remove_follow(self):
        self.assertEqual(Follow.objects.count(), 0)
        Follow.objects.create(
            author=FollowTest.author,
            user=FollowTest.follower
        )
        self.assertEqual(Follow.objects.count(), 1)
        client_follower = Client()
        client_follower.force_login(FollowTest.follower)
        client_follower.get(
            reverse(
                'posts:profile_unfollow',
                args=(FollowTest.author.username,)
            )
        )
        self.assertEqual(Follow.objects.count(), 0)
        follows = Follow.objects.filter(
            author=FollowTest.author,
            user=FollowTest.follower)
        self.assertFalse(follows)
