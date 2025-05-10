
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import AboutUs, TeamMember, ContactSubmission
from Register.models import CustomUser, Profile
from Blog.models import BlogPost
from renter.models import Order, Cart, Booking
from chat.models import ChatMessage
from notifications.models import Review, Notification
from owner.models import Item, ItemImage
from Payment.models import RentalPlan

# Custom Admin Site Configuration
admin.site.site_header = "MeroVada Admin Dashboard"
admin.site.site_title = "MeroVada Admin"
admin.site.index_title = "Welcome to MeroVada Administration"

# Utility function for emails
def send_email(subject, message, recipient):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

# Inline for Item Images
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('image', 'created_at')
    readonly_fields = ('created_at',)

# Model Admin Classes
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('message', 'sender__username', 'receiver__username')
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

# Removed duplicate AboutUsAdmin definition to resolve the conflict.

# Duplicate definition removed to avoid conflict

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message_preview', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('message', 'user__username')
    actions = ['mark_as_read', 'mark_as_unread']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

@admin.register(RentalPlan)
class RentalPlanAdmin(admin.ModelAdmin):
    list_display = ('renter', 'item', 'payment_frequency', 'amount_due', 'start_date', 'is_active')
    list_filter = ('payment_frequency', 'is_active', 'start_date')
    search_fields = ('renter__username', 'item__name')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'email_verified', 'is_staff')
    list_filter = ('role', 'email_verified', 'is_staff')
    search_fields = ('username', 'email')
    list_editable = ('role', 'email_verified')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'total_price')
    search_fields = ('user__username', 'item__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'renter', 'item', 'total_price', 'status', 'created_at', 'transaction_id')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('renter__username', 'item__name', 'transaction_id')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'transaction_id')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'published_at')
    list_filter = ('status', 'created_at', 'author__role')
    search_fields = ('title', 'content', 'author__username')
    actions = ['approve_posts']
    
    def approve_posts(self, request, queryset):
        queryset.update(status='approved', published_at=timezone.now())
        self.message_user(request, "Selected blog posts have been approved.")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'comment', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'item__name', 'comment')
    actions = ['approve_reviews', 'reject_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} reviews have been approved.")
    def reject_reviews(self, request, queryset):
        queryset.delete()
        self.message_user(request, f"{queryset.count()} reviews have been rejected.")

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at', 'category')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'owner__username')
    actions = ['approve_items', 'reject_items']
    inlines = [ItemImageInline]
    
    def approve_items(self, request, queryset):
        queryset.update(status='Approved')
        for item in queryset:
            send_email(f'Item Approved', f'Your item "{item.name}" has been approved.', item.owner.email)
    
    def reject_items(self, request, queryset):
        queryset.update(status='Rejected')
        for item in queryset:
            send_email(f'Item Rejected', f'Your item "{item.name}" has been rejected.', item.owner.email)
            
            
            
# cms/admin.py
from django.contrib import admin
from .models import AboutUs, TeamMember, ContactSubmission

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'mission_title', 'vision_title', 'story_title')
    list_editable = ('hero_title',)
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_description')
        }),
        ('Mission Section', {
            'fields': ('mission_title', 'mission_description')
        }),
        ('Vision Section', {
            'fields': ('vision_title', 'vision_description')
        }),
        ('Story Section', {
            'fields': ('story_title', 'story_description', 'story_image')
        }),
    )
    def has_add_permission(self, request):
        return not AboutUs.objects.exists()

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'photo')
    list_filter = ('role',)
    search_fields = ('name', 'role', 'bio')
    list_editable = ('role',)
    fields = ('name', 'role', 'bio', 'photo')

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)
    fields = ('name', 'email', 'message', 'submitted_at')
    def has_add_permission(self, request):
        return False
    
from django.contrib import admin
from .models import JobPosting, CompanyCulture, Benefit

# Customize admin classes to restrict access (optional)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employment_type', 'is_active', 'created_at')
    list_filter = ('employment_type', 'is_active')
    search_fields = ('title', 'description')

class CompanyCultureAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class BenefitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# Register models with admin
admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(CompanyCulture, CompanyCultureAdmin)
admin.site.register(Benefit, BenefitAdmin)