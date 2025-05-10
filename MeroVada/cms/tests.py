from django.test import TestCase, Client
from django.urls import reverse
from .models import AboutUs, ContactSubmission
from .form import JobPostingForm, BenefitForm

class AboutUsContactTests(TestCase):
    def setUp(self):
        self.client = Client()

    # def test_about_us_view(self):
    #     response = self.client.get(reverse('about_us'))  
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('about_us', response.context)
    #     self.assertIn('team_members', response.context)

    def test_contact_support_submission(self):
        response = self.client.post(reverse('contact_support'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(ContactSubmission.objects.filter(email='test@example.com').exists())

    def test_job_posting_form_valid(self):
        form = JobPostingForm(data={
            'title': 'Backend Developer',
            'location': 'Kathmandu',
            'employment_type': 'Full-Time',
            'description': 'Develop backend services.',
            'is_active': True
        })
        self.assertTrue(form.is_valid())

    def test_benefit_form_invalid_missing_title(self):
        form = BenefitForm(data={
            'description': 'Flexible hours',
        })
        self.assertFalse(form.is_valid())

    def test_about_us_model_str(self):
        about = AboutUs.objects.create()
        self.assertEqual(str(about), "About Us Content")
