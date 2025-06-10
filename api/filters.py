import django_filters
from .models import Anemometer
from django.db.models import Q, QuerySet
from django_filters.filters import CharFilter


class AnemometerFilter(django_filters.FilterSet):
    tags = CharFilter(
        method="filter_tags", help_text="Filter by tags (comma-separated)."
    )

    class Meta:
        model = Anemometer
        fields = ["tags"]

    def filter_tags(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        Filters the queryset based on a comma-separated list of tags.
        """
        tag_list = [tag.strip() for tag in value.split(",") if tag.strip()]
        if tag_list:
            query = Q()
            for tag in tag_list:
                query |= Q(tags__icontains=tag)
            return queryset.filter(query)
        return queryset
