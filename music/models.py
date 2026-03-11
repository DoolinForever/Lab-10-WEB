import os
import uuid
from django.db import models


class GenreAudience(models.TextChoices):
    GENERAL = 'general', 'Для всех'
    ADULTS = 'adults', 'Взрослая аудитория'
    KIDS = 'kids', 'Детская аудитория'


class PublishedGenreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    audience = models.CharField(
        max_length=20,
        choices=GenreAudience.choices,
        default=GenreAudience.GENERAL,
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    published = PublishedGenreManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


def track_image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'tracks/{uuid.uuid4().hex}{ext}'


class Track(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    duration = models.PositiveIntegerField(help_text='Длительность, сек')
    release_year = models.PositiveSmallIntegerField()
    play_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='tracks')
    tags = models.ManyToManyField(Tag, related_name='tracks', blank=True)
    image = models.ImageField(upload_to=track_image_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['-release_year', 'title']
        verbose_name = 'трек'
        verbose_name_plural = 'треки'

    def __str__(self):
        return self.title


class TrackDetails(models.Model):
    track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name='details')
    lyrics_author = models.CharField(max_length=150, blank=True)
    bpm = models.PositiveSmallIntegerField(null=True, blank=True)
    has_video = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'детали трека'
        verbose_name_plural = 'детали треков'

    def __str__(self):
        return f'Детали {self.track.title}'
