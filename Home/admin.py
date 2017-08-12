from django.contrib import admin
from .models import UserProfile,Book,Genre,PersonalCollection,Chapter,Forum,Thread,LikedBook
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(PersonalCollection)
admin.site.register(Chapter)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(LikedBook)
