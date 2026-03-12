from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0004_alter_track_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name='tracks',
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор',
            ),
        ),
    ]
