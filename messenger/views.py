from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def inbox(request):
    msgs = Message.objects.filter(recipient=request.user)
    return render(request, 'messenger/inbox.html', {'messages_': msgs})

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, 'Mensaje enviado')
            return redirect('messenger_inbox')
    else:
        initial = {}
        if 'to' in request.GET:
            initial['recipient'] = User.objects.get(username=request.GET['to'])
        if 'subject' in request.GET:
            initial['subject'] = request.GET['subject']
        form = MessageForm(initial=initial)

    return render(request, 'messenger/compose.html', {'form': form})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk, recipient=request.user)
    if not msg.read:
        msg.read = True
        msg.save(update_fields=['read'])
    return render(request, 'messenger/detail.html', {'msg': msg})
