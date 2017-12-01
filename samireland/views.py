"""Views for samireland.com"""

import django.shortcuts as shortcuts

def home(request):
    return shortcuts.render(request, "home.html")
