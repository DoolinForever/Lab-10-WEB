import os
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse


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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tracks',
        verbose_name='автор',
    )

    class Meta:
        ordering = ['-release_year', 'title']
        verbose_name = 'трек'
        verbose_name_plural = 'треки'
        permissions = [
            ('can_publish_track', 'Can publish track'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('track_detail', kwargs={'slug': self.slug})


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


class Comment(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='track_comments',
        verbose_name='автор',
    )
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        author = self.author or 'Аноним'
        return f'Комментарий от {author} к {self.track}'


class TrackLike(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='likes', verbose_name='трек')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='track_likes',
        verbose_name='пользователь',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'лайк трека'
        verbose_name_plural = 'лайки треков'
        constraints = [
            models.UniqueConstraint(fields=['track', 'user'], name='unique_track_user_like'),
        ]

    def __str__(self):
        return f'Лайк {self.user} → {self.track}'
