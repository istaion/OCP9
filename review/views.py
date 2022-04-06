from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from authentication.models import User


@login_required
def feed(request):
    tickets = models.Ticket.objects.filter(user = request.user)
    reviews = models.Review.objects.filter(user = request.user)
    context = {
        'reviews': reviews,
        'tickets': tickets,
    }
    return render(request, 'review/feed.html', context=context)


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


@login_required
def review_add(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'review/review_add.html', context=context)


@login_required
def review_response(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    return render(request, 'review/review_add.html', context=context)
