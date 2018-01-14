"""Media app views"""

import django.shortcuts as shortcuts
from django.contrib.auth.decorators import login_required

def media(request):
    return shortcuts.render(request, "media.html")
