from django.contrib import admin
from .models import Post, Category,Contact,Comment,Question
#scrap imports
from .models import ScrapData
from .models import URL


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'body','created_on')
    list_filter = ("created_on",)

class CategoryAdmin(admin.ModelAdmin):
    pass
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'projectDetails')
#######coments block##########
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'shortened_url')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'ans')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(ScrapData)
admin.site.register(URL, URLAdmin)
admin.site.register(Question, QuestionAdmin)