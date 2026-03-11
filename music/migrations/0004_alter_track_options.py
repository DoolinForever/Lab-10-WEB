from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_track_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={
                'ordering': ['-release_year', 'title'],
                'permissions': [('can_publish_track', 'Can publish track')],
                'verbose_name': 'трек',
                'verbose_name_plural': 'треки',
            },
        ),
    ]
