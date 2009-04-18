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
    raw_id_fields = ['folder']
    
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'folder', 'published_at')
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options'),
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
            'fields': ('name','caption', 'folder', 'published_at')
        }),
        ("Image", {
            'fields': ('image',) 
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Photo, PhotoAdmin)

class VideoAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'folder', 'published_at')
        }),
        ("Details", {
            'fields': ('url','image') 
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options'),
            'classes': ('collapse',)
        }),
    )
admin.site.register(Video, VideoAdmin)

class AudioAdmin(MediaAdmin):
    list_filter = ['created_at']
    fieldsets = (
        ("Basics", {
            'fields': ('name','caption', 'folder', 'published_at')
        }),
        ("Details", {
            'fields': ('file',) 
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug','comment_options'),
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