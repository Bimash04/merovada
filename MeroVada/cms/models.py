from django.db import models

class AboutUs(models.Model):
    hero_title = models.CharField(max_length=200, default="About MeroVada")
    hero_description = models.TextField(default="Your trusted partner in connecting owners and renters for a seamless, sustainable rental experience across Nepal and beyond.")
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_description = models.TextField(default="MeroVada is dedicated to empowering individuals and businesses by offering a reliable, user-friendly platform for renting and sharing resources.")
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_description = models.TextField(default="We aspire to lead the global shift toward a sharing economy, where resources are maximized, waste is minimized, and communities thrive.")
    story_title = models.CharField(max_length=200, default="Our Story")
    story_description = models.TextField(default="Established in 2023, MeroVada was born from a vision to revolutionize how people access and share resources.")
    story_image = models.ImageField(upload_to='about_us/', blank=True, null=True)

    def __str__(self):
        return "About Us Content"

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        
        
        
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        
        
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
    

# Job Posting Model
class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Remote', 'Remote')])
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"


# Culture Model (for "Our Culture")
class CompanyCulture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='culture_images/', blank=True, null=True, help_text="Upload an image for this culture item")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Company Culture"
        verbose_name_plural = "Company Culture"

# Benefit Model (for "Why Work With Us?")
class Benefit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='benefit_images/', blank=True, null=True, help_text="Upload an image for this benefit")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"