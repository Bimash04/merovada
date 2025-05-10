from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import BlogPost

User = get_user_model()

class BlogViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create some blog posts
        self.post1 = BlogPost.objects.create(
            title='Approved Post',
            content='This is an approved post.',
            author=self.user,
            status='approved'
        )
        self.post2 = BlogPost.objects.create(
            title='Pending Post',
            content='This is a pending post.',
            author=self.user,
            status='pending'
        )

    def test_blog_list_view(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_list.html')
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title) 
        

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_detail.html')
        self.assertContains(response, self.post1.title)

    def test_blog_detail_view_invalid_post(self):
        response = self.client.get(reverse('blog_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

 

    def test_submit_blog_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('submit_blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_blog.html')

    def test_submit_blog_view_post_valid(self):
        self.client.login(username='testuser', password='password')
        form_data = {
            'title': 'New Blog Title',
            'content': 'New blog content here.'
        }
        response = self.client.post(reverse('submit_blog'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after submission
        self.assertRedirects(response, reverse('blog_list'))
        self.assertTrue(BlogPost.objects.filter(title='New Blog Title').exists())

    def test_submit_blog_view_post_empty_fields(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('submit_blog'), data={})

        # Instead of response, access form errors via context
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)
