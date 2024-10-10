from rest_framework.serializers import Serializer, CharField


class SummarizeRequestSerializer(Serializer):
    slug = CharField(write_only=True)
    lang = CharField(write_only=True)


class SummarizeResponseSerializer(Serializer):
    summary = CharField(read_only=True)
