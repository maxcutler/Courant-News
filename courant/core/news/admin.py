from django.contrib import admin
from courant.core.news.models import *

from courant.core.dynamic_models.admin import AttributeInline

import notifications

class IssueArticleInline(admin.TabularInline):
    model = IssueArticle
    raw_id_fields = ('article',)
    extra = 10


class IssueAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_at'
    list_display = ['name', 'display_type', 'published_at', 'published']
    list_filter = ['display_type', 'published']
    search_fields = ['name']
    raw_id_fields = ('lead_media',)

    fieldsets = (
        ('General', {
            'fields': ('name', 'display_type')
        }),
        ('Publishing Settings', {
            'fields': ('published_at', 'published')
        }),
        ('Media', {
            'fields': ('lead_media',)
        })
    )
    
    inlines = (IssueArticleInline,)
    
    actions = ('send_email_update', )

    def send_email_update(self, request, queryset):
        for issue in queryset:
            options = {
                'subject': u'YDN Headlines: %s' % (issue.published_at.strftime("%B %d, %Y")),
                'from_address': 'headlines@yaledailynews.com',
                'from_name': 'Yale Daily News',
                'data': issue,
                'text_template': 'issues/email.txt',
                'html_template': 'issues/email.html'
            }
            count = notifications.send_email_update(**options)
            self.message_user(request, "Email update submitted. %d emails queued for delivery." % count)
    send_email_update.short_description = 'Send email update'
admin.site.register(Issue, IssueAdmin)


class DisplayTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'template_name': ("name",)}
admin.site.register(IssueDisplayType, DisplayTypeAdmin)
admin.site.register(ArticleDisplayType, DisplayTypeAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ['indented_name']
    ordering = ['full_path']
    prepopulated_fields = {'path': ('name',)}
admin.site.register(Section, SectionAdmin)


class ArticleStatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(ArticleStatus, ArticleStatusAdmin)


class ArticleBylineInline(admin.TabularInline):
    model = ArticleByline
    fields = ('staffer', 'order')
    raw_id_fields = ("staffer",)


class ArticleMediaInline(admin.TabularInline):
    model = ArticleMedia
    fields = ('media_item', 'order')
    raw_id_fields = ('media_item',)


class ArticleIssueInline(admin.TabularInline):
    model = IssueArticle
    raw_id_fields = ('issue',)
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_at'
    list_display = ['heading', 'section', 'published_at', 'status', 'dynamic_type']
    list_filter = ['published_at', 'status', 'display_type', 'section','dynamic_type']
    search_fields = ['heading']
    prepopulated_fields = {'slug': ('heading',)}

    fieldsets = (
        ("Basics", {
            'fields': ('dynamic_type', 'section', 'display_type', 'status', 'published_at')
        }),
        ("Article Contents", {
            'fields': ('heading', 'subheading', 'summary', 'body')
        }),
        ("Tags", {
            'fields': ('tags',)
        }),
        ("Advanced", {
            'fields': ('slug', 'comment_options'),
            'classes': ('collapse',)
        }),
    )

    inlines = [
        ArticleBylineInline,
        ArticleMediaInline,
        ArticleIssueInline,
        AttributeInline,
    ]
    
    actions = ('send_email_update', )

    def send_email_update(self, request, queryset):
        for article in queryset:
            options = {
                'subject': u'YDN Update: %s' % article.heading,
                'from_address': 'headlines@yaledailynews.com',
                'from_name': 'Yale Daily News',
                'data': article,
                'text_template': 'articles/email.txt',
                'html_template': 'articles/email.html'
            }
            count = notifications.send_email_update(**options)
            self.message_user(request, "Email update submitted. %d emails queued for delivery." % count)
    send_email_update.short_description = 'Send email update'
    
admin.site.register(Article, ArticleAdmin)

# Remove the admin section for tagging's TaggedItem model,
# since it is not useful for users
admin.site.unregister(tagging.models.TaggedItem)
