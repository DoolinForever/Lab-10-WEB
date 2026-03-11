from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_tag_track_trackdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=music.models.track_image_upload_to),
        ),
    ]
