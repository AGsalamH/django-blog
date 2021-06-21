from django.contrib import admin
from .models import Author, Post, Tag, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('posted_at', 'updated_at')
    prepopulated_fields ={'slug': ('title',)}
    list_display = ('title',)
    list_filter = ('tags',)
    


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'post')
    readonly_fields = ('created_at',)


# admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)
