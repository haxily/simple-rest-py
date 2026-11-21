import django_filters

from .models import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    min_age = django_filters.NumberFilter(field_name="age", lookup_expr="gte")
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr="lte")

    class Meta:
        model = User
        fields = ["name", "min_age", "max_age"]
