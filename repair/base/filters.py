import django_filters
from .models import *
  


class HandyManFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='user.username', lookup_expr='startswith')
    location = django_filters.CharFilter(field_name='location', lookup_expr='exact')

    class Meta:
        model = HandyMan
        fields = ['name','location']



class OrderFilter(django_filters.FilterSet):
    accepted = django_filters.BooleanFilter(field_name='accepted')
    completed = django_filters.BooleanFilter(field_name='completed')

    class Meta:
        model = Order
        fields = ['accepted','completed']
