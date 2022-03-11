from django.contrib import admin
from .models import Group, Post, Follow, Comment
# Registration of PostAdmin and GroupAdmin models.


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description', )
    search_fields = ('title',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    search_fields = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'author', )
    search_fields = ('text',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)
