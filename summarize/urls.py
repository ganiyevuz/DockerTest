from django.urls import path
from django.views.decorators.cache import cache_page

from conf.settings import CACHE_TTL, CACHE_KEY
from summarize.views import SummarizeGenericAPIView

urlpatterns = [
    path('summarize-articles/<str:lang>/<str:slug>', cache_page(CACHE_TTL, key_prefix=CACHE_KEY)(SummarizeGenericAPIView.as_view()),
         name='summarize'),
    # path('summarize-articles/<str:lang>/<str:slug>', SummarizeGenericAPIView.as_view(),
    #      name='summarize'),
]
