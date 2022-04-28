from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from . import forms
from . import models


@login_required
def feed(request):
    user_tickets = models.Ticket.objects.filter(user=request.user)
    other_tickets = models.Ticket.objects.filter(user__in=request.user.follows.all())
    reviews = models.Review.objects.filter(Q(user__in=request.user.follows.all()) |
                                           Q(user=request.user) | Q(ticket__in=user_tickets))
    tickets_and_reviews = sorted(
        chain(user_tickets, other_tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'review/feed.html', context=context)


@login_required
def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'review/posts.html', context=context)


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
            ticket.contributors.add(request.user, through_defaults={'review': review})
            ticket.save()
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
            ticket.contributors.add(request.user, through_defaults={'review': review})
            ticket.save()
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
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('feed')
    context = {
        'edit_form': edit_form,
        'review': review,
    }
    return render(request, 'review/review_update.html', context=context)


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('feed')
    context = {
        'edit_form': edit_form,
        'ticket': ticket
    }
    return render(request, 'review/ticket_update.html', context=context)


@login_required
def follow_users(request):
    following = request.user.following.all()
    followed_by = request.user.followed_by.all()
    follow_form = forms.UserFollowsForm(request_user=request.user)
    if request.method == 'POST':
        follow_form = forms.UserFollowsForm(request.POST, request_user=request.user)
        if follow_form.is_valid():
            follow_form.save()
            return redirect('follow_users')
    context = {
        'follow_form': follow_form,
        'following': following,
        'followed_by': followed_by,
    }
    return render(request, 'review/follow_users.html', context=context)

@login_required
def stop_follow(request, follow_id):
    follow = get_object_or_404(models.UserFollows, id=follow_id)
    followed_user = follow.followed_user
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


@login_required
def object_delete(request, instance_id, object_type):
    if object_type == 'Ticket':
        instance = get_object_or_404(models.Ticket, id=instance_id)
        delete_form = forms.DeleteTicketForm()
        if request.method == 'POST':
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                instance.delete()
                return redirect('feed')
    else:
        instance = get_object_or_404(models.Review, id=instance_id)
        delete_form = forms.DeleteReviewForm()
        if request.method == 'POST':
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                instance.delete()
                return redirect('feed')
    context = {
        'instance': instance,
        'delete_form': delete_form,
    }
    return render(request, 'review/delete.html', context=context)
