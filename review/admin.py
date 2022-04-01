from django.contrib import admin

from authentication.models import User
from review.models import Ticket

admin.site.register(Ticket)
admin.site.register(User)
