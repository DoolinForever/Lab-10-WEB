from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'track',
                    models.ForeignKey(on_delete=models.CASCADE, related_name='likes', to='music.track', verbose_name='трек'),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name='track_likes',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'лайк трека',
                'verbose_name_plural': 'лайки треков',
            },
        ),
        migrations.AddConstraint(
            model_name='tracklike',
            constraint=models.UniqueConstraint(fields=('track', 'user'), name='unique_track_user_like'),
        ),
    ]
