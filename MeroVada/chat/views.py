from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Register.models import CustomUser
from .models import ChatMessage
from django.db.models import Q
from django.http import JsonResponse

@login_required
def chat_list(request, other_user_id=None):

    chats = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    # Build a dictionary of conversation partners to deduplicate
    conversation_partners = {}
    for chat in chats:
        partner = chat.receiver if chat.sender == request.user else chat.sender
        conversation_partners[partner.id] = partner
    partners = list(conversation_partners.values())

    # Handle AJAX search request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_term = request.GET.get('search', '').strip()
        if search_term:
            # Filter partners by username
            partners = [
                partner for partner in partners
                if search_term.lower() in partner.username.lower()
            ]
        # Prepare data for JSON response
        partners_data = []
        for partner in partners:
            # Find the last message for this partner
            last_message = next(
                (chat for chat in chats if (chat.sender == request.user and chat.receiver == partner) or (chat.sender == partner and chat.receiver == request.user)),
                None
            )
            partners_data.append({
                'id': partner.id,
                'username': partner.username,
                # 'profile_picture': partner.profile_picture.url if partner.profile_picture else None,
                'last_message': {
                    'message': last_message.message if last_message else "Start a conversation...",
                    'is_sender': last_message.sender == request.user if last_message else False,
                    'timestamp': last_message.timestamp.strftime('%Y-%m-%d %H:%M:%S') if last_message else None,
                }
            })
        return JsonResponse({'partners': partners_data})

    # If a specific user is selected, fetch their conversation
    other_user = None
    messages = []
    room_id = None
    if other_user_id:
        other_user = get_object_or_404(CustomUser, id=other_user_id)
        messages = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('timestamp')
        room_id = "_".join(sorted([str(request.user.id), str(other_user.id)]))

    return render(request, 'chat_list.html', {
        'partners': partners,
        'other_user': other_user,
        'chats': messages,
        'room_id': room_id,
    })