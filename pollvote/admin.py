from django.contrib import admin
from .models import User, Region, Candidates, Competition,PollVote
# Register your models here.

admin.site.register(User)
admin.site.register(Region)
admin.site.register(Candidates)
admin.site.register(Competition)
admin.site.register(PollVote)




