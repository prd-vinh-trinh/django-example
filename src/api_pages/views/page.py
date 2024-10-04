from rest_framework.response import Response
from rest_framework.decorators import action
from api_pages.models.page import Page
from api_pages.serializer.page import PageSerializer
from base.views.base import BaseViewSet
from django.utils.translation import gettext as _

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class PageViewSet(BaseViewSet):
    queryset = Page.objects
    serializer_class = PageSerializer

    def create(self, request, *args, **kwangs):
        data = request.data
        data['author'] = str(request.user.id)
        print(data)
        serializer = PageSerializer(data=data)

        if serializer.is_valid():
            try:
                page = serializer.save()
                return Response({
                    "message": _("Page registered successfully."),
                }, status=HTTP_201_CREATED)
            except Exception as e:
                serializer.delete(page)
                return Response({"Error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        page = Page.objects(id__e="66fcea9e677baf3a2af4f5c1")
        return Response(page, status=HTTP_400_BAD_REQUEST)

    @action(methods="post", detail=True, url_path="comment")
    def comment(self, request, *args, **kwargs):
        data = request.data
        print(kwargs)
        data['author'] = str(request.user.id)
        serializer = PageSerializer(data=data)

        if serializer.is_valid():
            try:
                page = serializer.save()
                return Response({
                    "message": _("Page registered successfully."),
                }, status=HTTP_201_CREATED)
            except Exception as e:
                serializer.delete(page)
                return Response({"Error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
