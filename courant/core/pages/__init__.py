from django.template import add_to_builtins

#Make page_url templatetag available everywhere
add_to_builtins('courant.core.pages.templatetags.page_url')