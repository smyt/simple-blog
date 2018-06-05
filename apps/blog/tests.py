"""Blog tests."""

from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G

from apps.blog.models import BlogPost, Tag


class BlogTestCase(TestCase):
    """Class for testing blog application."""

    def setUp(self):
        """Adding creating superuser to each test."""
        super().setUp()
        self.user = User.objects.create_superuser(username='user', email='mail@mail.com', password='1')

    def test_empty_index(self):
        """Test working empty site."""
        r = self.client.get("/")
        self.assertEqual(0, len(r.context_data['posts']))
        self.assertEqual(None, r.context_data['last_published'])
        self.assertEqual(False, r.context_data['has_more'])

    def test_index_with_posts(self):
        """Test working blog with some posts."""
        posts = []
        start_date = datetime(2018, 2, 1)
        for x in range(5):
            posts.append(G(
                BlogPost,
                short_description="Short description {}".format(x),
                title='Title {}'.format(x),
                author=self.user.author,
                published_at=start_date + timedelta(x),
                is_published=True
            ))

        for x in range(7):
            posts.append(G(
                BlogPost,
                short_description="Short description hidden {}".format(x),
                title='Title hidden {}'.format(x),
                author=self.user.author,
                published_at=start_date + timedelta(5 + x),
                is_published=False
            ))

        r = self.client.get("/")

        self.assertEqual("{:%Y.%d.%m %H:%M:%S}".format(start_date), r.context_data['last_published'])
        self.assertEqual(False, r.context_data['has_more'])

        for x in range(5):
            self.assertIn("Short description {}".format(x), r.content.decode('utf8'))
            self.assertIn("Title {}".format(x), r.content.decode('utf8'))

        for x in range(7):
            self.assertNotIn("Short description hidden {}".format(x), r.content.decode('utf8'))
            self.assertNotIn("Title hidden {}".format(x), r.content.decode('utf8'))

        self.assertEqual(5, len(r.context_data['posts']))

    def test_filter_by_author(self):
        """Test filtering blog posts by author."""
        user2 = User.objects.create_superuser(username='user2', email='mail2@mail.com', password='1')

        post1 = G(BlogPost, author=self.user.author, title="user1 post", is_published=True)
        post2 = G(BlogPost, author=user2.author, title="user2 post", is_published=True)

        r = self.client.get("/author/{}/".format(self.user.pk))
        posts = r.context_data['posts']
        self.assertEqual(1, len(posts))
        self.assertEqual(post1.id, posts[0].id)

        r = self.client.get("/author/{}/".format(user2.pk))
        posts = r.context_data['posts']
        self.assertEqual(1, len(posts))
        self.assertEqual(post2.id, posts[0].id)

    def test_filter_by_tag(self):
        """Test filtering blog posts by tag."""
        tag1 = G(Tag, title='tag1', slug='tag1')
        tag2 = G(Tag, title='tag2', slug='tag2')

        start_date = datetime(2018, 1, 1)

        post_with_tags = G(BlogPost, is_published=True, author=self.user.author, published_at=start_date)
        post_with_tags.tags.add(tag1, tag2)

        post_tag1 = G(BlogPost, is_published=True, author=self.user.author, published_at=start_date + timedelta(1))
        post_tag1.tags.add(tag1)

        post_tag2 = G(BlogPost, is_published=True, author=self.user.author, published_at=start_date + timedelta(2))
        post_tag2.tags.add(tag2)

        r = self.client.get("/tag/{}/".format(tag1.slug))
        posts = r.context_data['posts']
        self.assertEqual(posts[1].id, post_with_tags.id)
        self.assertEqual(posts[0].id, post_tag1.id)

        r = self.client.get("/tag/{}/".format(tag2.slug))
        posts = r.context_data['posts']
        self.assertEqual(posts[1].id, post_with_tags.id)
        self.assertEqual(posts[0].id, post_tag2.id)

    def test_index_with_more_posts_than_one_page_can_hold(self):
        """Test index page with count pages more than one page can has."""
        start_date = datetime(2018, 1, 13)
        posts = []
        for x in range(10 + 5):
            posts.append(G(
                BlogPost,
                short_description="Short description {}".format(x),
                title='Title {}'.format(x),
                author=self.user.author,
                published_at=start_date + timedelta(x),
                is_published=True
            ))

        r = self.client.get("/")

        self.assertEqual("{:%Y.%d.%m %H:%M:%S}".format(start_date + timedelta(5)), r.context_data['last_published'])
        self.assertEqual(True, r.context_data['has_more'])
        self.assertEqual(10, len(r.context_data['posts']))

        last_published = r.context_data['last_published']
        r = self.client.get("/", {
            'lastPublished': last_published
        })

        self.assertEqual("{:%Y.%d.%m %H:%M:%S}".format(start_date), r.context_data['last_published'])
        self.assertEqual(False, r.context_data['has_more'])
        self.assertEqual(5, len(r.context_data['posts']))

        r = self.client.get("/", {
            'lastPublished': last_published
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual("{:%Y.%d.%m %H:%M:%S}".format(start_date), r.json()['lastPublished'])
        self.assertEqual(False, r.json()['has_more'])
        self.assertIsNotNone(r.json()['content'])

    def test_post_page(self):
        """Test adding post to blog."""
        start_date = datetime(2018, 1, 13)
        post = G(
            BlogPost,
            short_description="Short description",
            title='Title',
            text='Long text',
            url="first_post",
            author=self.user.author,
            published_at=start_date,
            is_published=True
        )

        r = self.client.get("/first_post/")
        r.content.decode('utf8')
        self.assertIn("Short description", post.short_description)
        self.assertIn("Title", post.title)
        self.assertIn("Long text", post.text)
