from rest_framework.exceptions import ValidationError, NotFound, ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from summarize.models import SummarizedArticle
from summarize.serializers import SummarizeRequestSerializer, SummarizeResponseSerializer
from summarize.functions import summarize, get_article


class SummarizeGenericAPIView(GenericAPIView):
    serializer_class = SummarizeRequestSerializer
    queryset = SummarizedArticle.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        slug = serializer.validated_data['slug']
        summarized_article = qs.filter(slug=slug).first()
        if summarized_article:
            return Response(SummarizeResponseSerializer(summarized_article).data)
        lang = serializer.validated_data['lang']
        article = get_article(slug, lang)
        if not article:
            raise NotFound("Article not found.")
        summary = summarize(text=article, lang=lang)
        if summary:
            instance = qs.create(slug=slug, summary=summary)
            return Response(SummarizeResponseSerializer(instance).data)
        raise ParseError("Failed to summarize the article.")
