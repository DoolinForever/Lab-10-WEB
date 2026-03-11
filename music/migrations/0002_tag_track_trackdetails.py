from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=120, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=160, unique=True)),
                ('duration', models.PositiveIntegerField(help_text='Длительность, сек')),
                ('release_year', models.PositiveSmallIntegerField()),
                ('play_count', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
                ('genre', models.ForeignKey(on_delete=models.CASCADE, related_name='tracks', to='music.genre')),
            ],
            options={
                'ordering': ['-release_year', 'title'],
                'verbose_name': 'трек',
                'verbose_name_plural': 'треки',
            },
        ),
        migrations.CreateModel(
            name='TrackDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lyrics_author', models.CharField(blank=True, max_length=150)),
                ('bpm', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('has_video', models.BooleanField(default=False)),
                ('track', models.OneToOneField(on_delete=models.CASCADE, related_name='details', to='music.track')),
            ],
            options={
                'verbose_name': 'детали трека',
                'verbose_name_plural': 'детали треков',
            },
        ),
        migrations.AddField(
            model_name='track',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tracks', to='music.tag'),
        ),
    ]
