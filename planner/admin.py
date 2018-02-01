from django.contrib import admin

# Register your models here.
from .models import User, Note

class NoteInline(admin.TabularInline):
    model = Note
    extra = 0

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Name', {'fields': ['first_name','last_name',]}),
    ('Birthday', {'fields': ['birthday']}),
    ('Motto', {'fields': ['motto']}),
    ]
    inlines = [NoteInline]

admin.site.register(User, UserAdmin)
admin.site.register(Note)
