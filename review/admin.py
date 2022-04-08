from django.contrib import admin

from authentication.models import User
from review.models import Ticket, UserFollows, Review

admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(UserFollows)
admin.site.register(Review)