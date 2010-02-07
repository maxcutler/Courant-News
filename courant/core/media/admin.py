from django.contrib import admin
from courant.core.media.models import *

class MediaFolderAdmin(admin.ModelAdmin):
    list_display = ['indented_name']
    search_fields = ['name']
    ordering = ('lft',)
admin.site.register(MediaFolder, MediaFolderAdmin)

class MediaBylineInline(admin.TabularInline):
    model = MediaByline
    fields = ('staffer','order')
    raw_id_fields = ('staffer',)

class MediaAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ['name', 'created_at', 'admin_thumbnail']
    list_display_links = ['name','admin_thumbnail']
    list_filter = ['created_at', 'content_type']
    list_per_page = 10
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        MediaBylineInline,
    ]
admin.site.register(MediaItem, MediaAdmin)

class PhotoAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("Image", {
            'fields': ('image',)
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Photo, PhotoAdmin)

class VideoAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("Details", {
            'fields': ('url','image')
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Video, VideoAdmin)

class AudioAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("Details", {
            'fields': ('file',)
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Audio, AudioAdmin)

class GalleryMediaInline(admin.TabularInline):
    model = GalleryMedia
    fields = ('media_item','order')
    raw_id_fields = ('media_item',)
    fk_name = 'gallery'

class GalleryAdmin(MediaAdmin):
    list_filter = ['created_at']
    inlines = [
        MediaBylineInline,
        GalleryMediaInline
    ]
admin.site.register(Gallery, GalleryAdmin)

class GalleryUploadAdmin(admin.ModelAdmin):
    raw_id_fields = ('staffer',)
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button
admin.site.register(GalleryUpload, GalleryUploadAdmin)


class FileAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("File", {
            'fields': ('file','image','width','height')
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(File, FileAdmin)

class HTMLMediaSnippetAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'published_at')
        }),
        ("Snippet", {
            'fields': ('snippet', 'image',)
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options', 'staffers_override', 'status_line_override'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(HTMLMediaSnippet, HTMLMediaSnippetAdmin)