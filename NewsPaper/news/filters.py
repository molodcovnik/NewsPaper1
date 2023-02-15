import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    header_post = django_filters.CharFilter(lookup_expr='icontains', label='Header post')

    category_post = ModelMultipleChoiceFilter(
        field_name='category_post',
        queryset= Category.objects.all(),
        label='Category',
        conjoined=False
    )

    category_type = django_filters.ChoiceFilter(
        field_name='category_type',
        label='Type',
        empty_label='Select a type',
        choices=Post.TYPE
    )

    time_add = DateTimeFilter(
        field_name='time_add',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y:%m:%d',
            attrs={'type': 'date'},
        )
    )
