import django_filters
from .models import *
  


class HandyManFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='user.username', lookup_expr='startswith')
    city = django_filters.CharFilter(field_name='user.city', lookup_expr='exact')
    # category = django_filters

    class Meta:
        model = HandyMan
        fields = ['name','city']



class OrderFilter(django_filters.FilterSet):
    accepted = django_filters.BooleanFilter(field_name='accepted')
    completed = django_filters.BooleanFilter(field_name='completed')

    class Meta:
        model = Order
        fields = ['accepted','completed']




class ReviewFilter(django_filters.FilterSet):
    username = django_filters.BooleanFilter(field_name='user__username')
    rating = django_filters.BooleanFilter(field_name='rating')

    class Meta:
        model = Review
        fields = ['username','rating']
