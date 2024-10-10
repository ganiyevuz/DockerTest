from django.db.models import Model, TextField, PositiveBigIntegerField, SlugField, DateTimeField, CharField


class SummarizedArticle(Model):
    slug = SlugField(primary_key=True, unique=True, max_length=256)
    lang = CharField(max_length=5)
    summary = TextField()
    created_at = DateTimeField(auto_now_add=True)
