from django import template
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.filter
def model_type(value):
    """
    to check if an object is a Ticket or a Review
    """
    return type(value).__name__


@register.filter
def get_posted_at_display(posted_at):
    """
    return str to indicate date posted
    """
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Publié il y a {int(seconds_ago // MINUTE)} minutes.'
    elif seconds_ago <= DAY:
        return f'Publié il y a {int(seconds_ago // HOUR)} heures.'
    return f'Publié le {posted_at.strftime("%d %b %y à %Hh%M")}'


@register.filter
def contributor_list(ticket):
    """
    return all users if they already answer to a ticket
    """
    contrib_list = ticket.contributors.all()
    return contrib_list
