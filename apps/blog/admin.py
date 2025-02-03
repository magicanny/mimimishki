from django.contrib import admin

from apps.blog.models import Post, Image


class InlineImage(admin.TabularInline):
    model = Image
    field = ('image', 'is_main', 'title', 'slug',)
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_editable = ('status',)
    list_display = ('author', 'title', 'created_date', 'status',)
    list_display_links = ('author', 'title',)
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (InlineImage,)

    def save_model(self, request, obj, form, change):
        """
        Author identification
        """
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
