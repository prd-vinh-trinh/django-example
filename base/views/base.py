from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from drf_nested_forms.utils import NestedForm


class BaseViewSet(viewsets.ModelViewSet):
    queryset_map = {}
    search_map = {}
    serializer_class = None
    required_alternate_scopes = {}

    def get_queryset(self):
        return self.queryset_map.get(self.action, self.queryset)

    def clear_querysets_cache(self):
        if self.queryset is not None:
            self.queryset._result_cache = None

        for action, queryset in self.queryset_map.items():
            queryset._result_cache = None


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = request.query_params

        keyword = params.get("keyword")
        if keyword and len(self.search_map) > 0:
            query = Q()
            for field, op in self.search_map.items():
                kwargs = {'{0}__{1}'.format(field, op): keyword}
                query |= Q(**kwargs)
            queryset = queryset.filter(query)

        if params.get('page_size') is not None:
            page = self.paginate_queryset(queryset)
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = self.get_serializer(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)
