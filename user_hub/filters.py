import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class SearchUserFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method="user_search_filter")

    def user_search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(email__iexact=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
        )