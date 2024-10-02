from api_pages.models.page import Page
from api_pages.serializer.page import PageSerializer
from base.views.base import BaseViewSet


class PageViewSet(BaseViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer