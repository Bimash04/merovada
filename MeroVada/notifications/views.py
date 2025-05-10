from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from owner.models import Item
from .models import Review, Notification


@login_required
def add_review(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        
        # Check if the item has an owner before creating a notification
        if not hasattr(item, 'owner') or not item.owner:
            messages.error(request, "The item has no owner to notify.")
            return redirect('product_detail', id=item_id)
        
        # Create and save the review (not approved by default)
        review = Review.objects.create(
            item=item,
            user=request.user,
            comment=comment,
            is_approved=False  # Default to False
        )
        
        # Create a notification for the item owner
        Notification.objects.create(
            user=item.owner,
            notification_type='review',
            message=f"{request.user.username} left a review on your item: {item.name}",
            item=item,
        )
        
        messages.success(request, "Your review has been submitted and is pending admin approval.")
        return redirect('product_desc', item_id=item_id)
    
    return redirect('product_desc', item_id=item_id)

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.mark_as_read()
    return redirect('notifications')

def product_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = Review.objects.filter(item=item, is_approved=True).order_by('-created_at')  # Only approved reviews
    recommended_items = Item.objects.filter(category=item.category).exclude(id=item.id)[:3]
    
    context = {
        'item': item,
        'reviews': reviews,
        'recommended_items': recommended_items,
    }
    
    return render(request, 'product_desc.html', context)



@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications')

@login_required
def edit_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    if request.method == 'POST':
        new_message = request.POST.get('message')
        notification.message = new_message
        notification.save()
        return redirect('notifications')
    
    return render(request, 'edit_notification.html', {'notification': notification})

def help_centre(request):
    return render(request, 'help_centre.html')


