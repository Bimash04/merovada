from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from owner.models import Item
from renter.models import Order
from .models import RentalPlan
import requests
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from notifications.models import Notification
from owner.models import Item
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from datetime import timedelta, date
from django.http import HttpResponse
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

logger = logging.getLogger(__name__)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def payment_failed(request):
    return render(request, 'payment_failed.html')

@login_required
def checkout(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.GET.get('quantity', 1))  # From URL query
    total_price = item.price * quantity

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        payment_frequency = request.POST.get('payment_frequency')  
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        # Validate payment_frequency
        if not payment_frequency:
            payment_frequency = 'monthly'  

        total_price = item.price * quantity  

        # Create order
        order = Order.objects.create(
            renter=request.user,
            item=item,
            quantity=quantity,
            total_price=total_price,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='pending',
        )

        # Calculate rental duration based on the selected plan
        rental_durations = {
            'weekly': 7,
            'fortnightly': 14,
            'monthly': 30,
            'quarterly': 90,
            'half_yearly': 180,
            'yearly': 365,
        }
        
        start_date = date.today()
        duration_days = rental_durations.get(payment_frequency, 30)  # Default to 30 if invalid
        end_date = start_date + timedelta(days=duration_days)

        # Store rental plan before payment verification
        rental = RentalPlan.objects.create(
            renter=request.user,
            item=item,
            start_date=start_date,
            end_date=end_date,
            payment_frequency=payment_frequency,  
            amount_due=total_price,
            last_payment_date=None,
            next_payment_date=start_date + timedelta(days=duration_days),
            is_active=False  # Set to active after payment confirmation
        )

        # Process Khalti Payment
        if payment_method == 'Khalti':
            khalti_url = "https://a.khalti.com/api/v2/epayment/initiate/"
            headers = {
                'Authorization': f'Key {settings.KHALTI_SECRET_KEY.strip()}',
                'Content-Type': 'application/json',
            }
            payload = {
                "return_url": request.build_absolute_uri(f"/verify-khalti/{order.id}/"),
                "website_url": request.build_absolute_uri('/'),
                "amount": int(total_price * 100),  # Convert to paisa
                "purchase_order_id": str(order.id),
                "purchase_order_name": item.name,
                "customer_info": {
                    "name": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                }
            }

            try:
                response = requests.post(khalti_url, headers=headers, json=payload)
                response_data = response.json()
                logger.info(f"Khalti API Response: {response_data}")

                if response.status_code == 200 and response_data.get('payment_url'):
                    order.pidx = response_data.get('pidx')
                    order.save()
                    return redirect(response_data.get('payment_url'))
                else:
                    order.status = 'Cancelled'
                    order.save()
                    return redirect('payment_failed')

            except requests.exceptions.RequestException as e:
                logger.error(f"Error with Khalti API: {e}")
                order.status = 'Failed'
                order.save()
                return redirect('payment_failed')

        # For non-Khalti (e.g., Cash on Delivery), redirect to confirmation
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'item': item,
        'quantity': quantity,
        'total_price': total_price
    })
    


@login_required
def verify_khalti(request, order_id):
    order = get_object_or_404(Order, id=order_id, renter=request.user)
    
    if order.status == 'completed':
        rental = RentalPlan.objects.filter(renter=request.user, item=order.item).first()
        return payment_success(request, order, rental)

    # Khalti verification API
    verify_url = "https://a.khalti.com/api/v2/epayment/lookup/"
    headers = {
        'Authorization': f'Key {settings.KHALTI_SECRET_KEY.strip()}',
        'Content-Type': 'application/json',
    }
    payload = {"pidx": order.pidx}

    try:
        response = requests.post(verify_url, headers=headers, json=payload)
        response_data = response.json()
        logger.info(f"Khalti Verification Response: {response_data}")

        if response.status_code == 200 and response_data.get('status') == 'Completed':
            # Mark order as completed
            order.status = 'completed'
            order.transaction_id = response_data.get('transaction_id', order.pidx)
            order.save()

            # Activate rental plan
            rental = RentalPlan.objects.filter(renter=request.user, item=order.item).first()
            if rental:
                rental.is_active = True
                rental.last_payment_date = date.today()
                rental.save()
            else:
                logger.error(f"No RentalPlan found for order {order.id}")

            return payment_success(request, order, rental)
        else:
            order.status = 'Failed'
            order.save()
            return redirect('payment_failed')

    except requests.exceptions.RequestException as e:
        logger.error(f"Khalti Verification Error: {e}")
        order.status = 'Failed'
        order.save()
        return redirect('payment_failed')


@login_required
def download_payment_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, renter=request.user, status='completed')
    rental = RentalPlan.objects.filter(renter=request.user, item=order.item).first()

    rental_durations = {
        'weekly': 7,
        'fortnightly': 14,
        'monthly': 30,
        'quarterly': 90,
        'half_yearly': 180,
        'yearly': 365,
    }
    rental_duration = rental_durations.get(rental.payment_frequency, 30) if rental else "N/A"

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Payment Confirmation", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Payment For: Renting {order.item.name}", styles['Normal']))
    story.append(Paragraph(f"Item Details: {order.item.description or 'No description available'}", styles['Normal']))
    story.append(Paragraph(f"Quantity: {order.quantity}", styles['Normal']))
    story.append(Paragraph(f"Amount Paid: Rs {order.total_price:.2f}", styles['Normal']))
    story.append(Paragraph(f"Rental Plan: {rental.payment_frequency.title() if rental else 'Not specified'} ({rental_duration} days)", styles['Normal']))
    story.append(Paragraph(f"Start Date: {rental.start_date.strftime('%B %d, %Y') if rental else 'Not specified'}", styles['Normal']))
    story.append(Paragraph(f"End Date: {rental.end_date.strftime('%B %d, %Y') if rental else 'Not specified'}", styles['Normal']))
    story.append(Paragraph(f"Transaction ID: {order.transaction_id or 'N/A'}", styles['Normal']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_confirmation_order_{order_id}.pdf"'
    return response




@login_required
def payment_success(request, order=None, rental=None):
    if not order:
        order = get_object_or_404(Order, renter=request.user, status='completed')
    
    if not rental:
        rental = RentalPlan.objects.filter(renter=request.user, item=order.item).first()

    rental_durations = {
        'weekly': 7,
        'fortnightly': 14,
        'monthly': 30,
        'quarterly': 90,
        'half_yearly': 180,
        'yearly': 365,
    }
    rental_duration = rental_durations.get(rental.payment_frequency, 30) if rental else "N/A"

    context = {
        'order_id': order.id,  
        'item': order.item,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'payment_frequency': rental.payment_frequency if rental else None,
        'rental_duration': rental_duration,
        'start_date': rental.start_date if rental else None,
        'end_date': rental.end_date if rental else None,
        'transaction_id': order.transaction_id,
        'renter': order.renter,
    }

    # Send email to renter (payment invoice)
    try:
        renter_email = order.renter.email.strip() if order.renter.email else None
        logger.debug(f"Preparing invoice email for renter: {renter_email} (username: {order.renter.username}, role: {order.renter.role})")
        if not renter_email:
            logger.error(f"Renter {order.renter.username} has no email address; skipping email")
        else:
            subject = f'Payment Confirmation for Order #{order.id}'
            logger.debug("Rendering payment_invoice.html")
            html_content = render_to_string('payment_invoice.html', context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [renter_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Payment Confirmation", styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Payment For: Renting {order.item.name}", styles['Normal']))
            story.append(Paragraph(f"Item Details: {order.item.description or 'No description available'}", styles['Normal']))
            story.append(Paragraph(f"Quantity: {order.quantity}", styles['Normal']))
            story.append(Paragraph(f"Amount Paid: Rs {order.total_price:.2f}", styles['Normal']))
            story.append(Paragraph(f"Rental Plan: {rental.payment_frequency.title() if rental else 'Not specified'} ({rental_duration} days)", styles['Normal']))
            story.append(Paragraph(f"Start Date: {rental.start_date.strftime('%B %d, %Y') if rental else 'Not specified'}", styles['Normal']))
            story.append(Paragraph(f"End Date: {rental.end_date.strftime('%B %d, %Y') if rental else 'Not specified'}", styles['Normal']))
            story.append(Paragraph(f"Transaction ID: {order.transaction_id or 'N/A'}", styles['Normal']))

            doc.build(story)
            pdf = buffer.getvalue()
            buffer.close()

            email.attach(f'payment_confirmation_order_{order.id}.pdf', pdf, 'application/pdf')
            logger.debug(f"Sending invoice email to {renter_email}")
            email.send()
            logger.info(f"Payment invoice email sent to renter: {renter_email}")
    except Exception as e:
        logger.error(f"Failed to send payment invoice email to {renter_email or 'unknown'}: {str(e)}")

    # Send notification and email to owner
    try:
        if hasattr(order.item, 'owner') and order.item.owner:
            owner_email = order.item.owner.email.strip() if order.item.owner.email else None
            logger.debug(f"Preparing notification for owner: {owner_email} (username: {order.item.owner.username}, role: {order.item.owner.role})")
            # Create notification
            Notification.objects.create(
                user=order.item.owner,
                notification_type='payment',
                message=f"A payment of Rs {order.total_price:.2f} has been made for renting your item: {order.item.name} by {order.renter.username}.",
                item=order.item,
            )
            logger.info(f"Notification created for owner: {order.item.owner.username}")
            if not owner_email:
                logger.error(f"Owner {order.item.owner.username} has no email address; skipping email")
            else:
                owner_subject = f"New Payment Received for {order.item.name}"
                owner_context = {
                    'item': order.item,
                    'renter': order.renter.username,
                    'total_price': order.total_price,
                    'quantity': order.quantity,
                    'order_id': order.id,
                    'transaction_id': order.transaction_id,
                    'owner': order.item.owner,
                }
                logger.debug("Rendering owner_payment_notification.html")
                owner_html_content = render_to_string('owner_payment_notification.html', owner_context)
                owner_text_content = strip_tags(owner_html_content)
                owner_email = EmailMultiAlternatives(
                    owner_subject,
                    owner_text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [owner_email]
                )
                owner_email.attach_alternative(owner_html_content, "text/html")
                logger.debug(f"Sending notification email to {owner_email}")
                owner_email.send()
                logger.info(f"Payment notification email sent to owner: {owner_email}")
        else:
            logger.error(f"No owner found for item: {order.item.name}")
    except Exception as e:
        logger.error(f"Failed to send payment notification to owner {owner_email or 'unknown'}: {str(e)}")

    logger.info(f"Rendering payment_sucess.html with context: {context}")
    return render(request, 'payment_sucess.html', context)