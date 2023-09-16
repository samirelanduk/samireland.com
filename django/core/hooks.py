import requests
from django.conf import settings
from django.db import transaction
from wagtail import hooks

def get_page_paths(page):
    paths = [page.url]
    try:
        paths += page.also_revalidate
    except AttributeError:
        pass
    return paths


def revalidate_paths(paths):
    for path in paths:
        webhook_url = f"{settings.INTERNAL_FRONTEND_URL}/api/revalidate"
        webhook_url += f"?path={path}&secret={settings.REVALIDATE_TOKEN}"
        requests.get(webhook_url)


@hooks.register("after_edit_page")
def after_edit_page(request, page):
    revalidate_paths(get_page_paths(page))


@hooks.register("after_create_page")
def after_create_page(request, page):
    revalidate_paths(get_page_paths(page))


@hooks.register("after_delete_page")
def after_delete_page(request, page):
    paths = get_page_paths(page)
    transaction.on_commit(lambda: revalidate_paths(paths))