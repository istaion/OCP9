from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from . import forms
from . import models


@login_required
def feed(request):
    tickets = models.Ticket.objects.filter(Q(user__in=request.user.follows.all()) | Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=request.user.follows.all()) | Q(user=request.user))
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'review/feed.html', context=context)


@login_required
def ticket_add(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
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
    return render(request, 'review/review_response.html', context=context)


@login_required
def review_update(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
        'review': review,
    }
    return render(request, 'review/review_update.html', context=context)


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/ticket_update.html', context=context)


@login_required
def follow_users(request):
    following = request.user.following.all()
    followed_by = request.user.followed_by.all()
    follow_form = forms.UserFollowsForm()
    if request.method == 'POST':
        follow_form = forms.UserFollowsForm(request.POST)
        if follow_form.is_valid():
            follow = follow_form.save(commit=False)
            follow.user = request.user
            follow.save()
            return redirect('follow_users')
    context = {
        'follow_form': follow_form,
        'following': following,
        'followed_by': followed_by,
    }
    return render(request, 'review/follow_users.html', context=context)

@login_required
def stop_follow(request, followed_user):
    follow = get_object_or_404(models.UserFollows, Q(user=request.user) | Q(followed_user=followed_user))
    stop_follow_form = forms.DeleteUserFollowsForm()
    if request.method == 'POST':
        stop_follow_form = forms.DeleteUserFollowsForm(request.POST)
        if stop_follow_form.is_valid():
            follow.delete()
            return redirect('follow_users')
    context = {
        'stop_follow_form': stop_follow_form,
        'followed_user': followed_user,
    }
    return render(request, 'review/follow_delete.html', context=context)
