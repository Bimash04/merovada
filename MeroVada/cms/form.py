from django import forms
from .models import JobPosting, CompanyCulture, Benefit,AboutUs
  
class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'location', 'employment_type', 'description', 'is_active']
class CompanyCultureForm(forms.ModelForm):
    class Meta:
        model = CompanyCulture
        fields = ['title', 'description', 'image'] 

class BenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = ['title', 'description', 'image']  
   



class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = [
            'hero_title', 'hero_description',
            'mission_title', 'mission_description',
            'vision_title', 'vision_description',
            'story_title', 'story_description', 'story_image'
        ]