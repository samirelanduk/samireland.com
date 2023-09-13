import requests
from django.conf import settings
from wagtail import hooks

@hooks.register("after_edit_page")
def after_edit_page(request, page):
    webhook_url = f"{settings.INTERNAL_FRONTEND_URL}/api/revalidate/"
    webhook_url += f"?path={page.url}&secret={settings.REVALIDATE_TOKEN}"
    requests.get(webhook_url)