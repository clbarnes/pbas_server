from django.conf.urls import url

from pbas.control import get_progress_bar, create_progress_bar, update_progress_bar

urlpatterns = [
    url(r'^create$', create_progress_bar),
    url(r'^(?P<code>\w+)/get$', get_progress_bar),
    url(r'^(?P<code>\w+)/update', update_progress_bar)
]
