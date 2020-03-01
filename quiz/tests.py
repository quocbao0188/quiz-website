from django.test import TestCase
from .models import Post
# Create your tests here.
class QuizTests(TestCase):
    def setUp(self):
        Post.objects.create(
            title = 'myTitle',
            body = 'Just a Test'
        )
    
    def test_str_representation(self):
        post = Post(title = 'My entry title')
        self.assertEqual(str(post), post.title)

    