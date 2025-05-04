import django_filters
from .models import Anemometer
from django.db.models import JSONField, Q, QuerySet
from django_filters.filters import BaseInFilter, CharFilter

class TagsFilter(BaseInFilter, CharFilter):
    pass

class AnemometerFilter(django_filters.FilterSet):
    # tags = TagsFilter(field_name='tags', lookup_expr='icontains')
    tags = CharFilter(method='filter_tags')

    class Meta:
        model = Anemometer
        fields = ['tags']
        filter_overrides = {
            JSONField: {
                'filter_class': CharFilter,
            },
        }

    def filter_tags(self, queryset: QuerySet, name, value: str) -> QuerySet:
        if "," in value:
            tag_list: list[str] =[tag.strip() for tag in value.split(",") if tag != ""]
            query = Q()
            for tag in tag_list:
                query |= Q(tags__icontains=tag)
            queryset: QuerySet = queryset.filter(query)
            return queryset
        else:
            return queryset.filter(tags__icontains=value)