from django.test import TestCase, Client
from django.urls import reverse
from cms.models import JobPosting, CompanyCulture, Benefit

class CareersViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        
        self.active_job = JobPosting.objects.create(title='Software Engineer', is_active=True)
        self.inactive_job = JobPosting.objects.create(title='Inactive Role', is_active=False)
        self.culture = CompanyCulture.objects.create(title='Innovation', description='We value innovation.')
        self.benefit = Benefit.objects.create(title='Health Insurance', description='We provide health benefits.')

    def test_careers_view_status_code(self):
        response = self.client.get(reverse('careers'))
        self.assertEqual(response.status_code, 200)

    def test_careers_template_used(self):
        response = self.client.get(reverse('careers'))
        self.assertTemplateUsed(response, 'careers.html')

    def test_careers_context_data(self):
        response = self.client.get(reverse('careers'))
        self.assertIn(self.active_job, response.context['jobs'])
        self.assertNotIn(self.inactive_job, response.context['jobs'])
        self.assertIn(self.culture, response.context['culture_items'])
        self.assertIn(self.benefit, response.context['benefits'])
