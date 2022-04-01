from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from authentication.models import User


@login_required
def feed(request):
    tickets = models.Ticket.objects.filter(user = request.user)
    return render(request, 'review/feed.html', context={'tickets': tickets})

@login_required
def ticket_add(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('feed')
    return render(request, 'review/ticket_add.html', context={'form': form})
