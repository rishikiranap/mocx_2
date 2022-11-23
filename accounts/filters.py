import django_filters

from .models import InterviewerAccount

class Listingfilter(django_filters.FilterSet):
    class Meta:
        model=InterviewerAccount
        fields={'Domain':['exact'],'Experience':['gt']}
