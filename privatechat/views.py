from django.shortcuts import render
from .models import PrivateMessage,PrivateChat
from .forms import PrivateMessageForm
from django.shortcuts import get_object_or_404

def chat(request):
    form = PrivateMessageForm()
    
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        
        if form.is_valid():
            chat_id = request.POST.get('chat_id')
            try:
                specific_chat_id = int(chat_id)
                specific_chat = get_object_or_404(PrivateChat, id=specific_chat_id)
                
                new_message = form.save(commit=False)
                new_message.user = request.user
                new_message.chat = specific_chat  # Assign the retrieved specific chat
                new_message.save()
                
                chat_messages = PrivateMessage.objects.filter(chat=specific_chat).order_by('created')
                context = {'chat_messages': chat_messages}
                
                return render(request, 'privatechat/privateroom.html', context)
            
            except ValueError:
                # Handle invalid chat_id (e.g., non-numeric ID)
                pass
    
    context = {'form': form}
    return render(request, 'privatechat/privateroom.html', context)
