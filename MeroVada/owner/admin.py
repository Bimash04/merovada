from django.contrib import admin
    
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Item

# @admin.action(description="Approve selected items")
# def approve_items(modeladmin, request, queryset):
#     queryset.update(status='Approved')
#     for item in queryset:
#         send_email(item, "Approved")

# @admin.action(description="Reject selected items")
# def reject_items(modeladmin, request, queryset):
#     queryset.update(status='Rejected')
#     for item in queryset:
#         send_email(item, "Rejected")

# def send_email(item, status):
#     """Helper function to send email notifications."""
#     send_mail(
#         f'Item {status}',
#         f'Your item "{item.name}" has been {status.lower()}.',
#         settings.EMAIL_HOST_USER,
#         [item.owner.email],
#         fail_silently=False,
#     )

# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner', 'status', 'created_at', 'category')
#     list_filter = ('status', 'category', 'created_at')
#     search_fields = ('name', 'owner__username')
#     actions = [approve_items, reject_items]
   

