# Generated manually to add views field to Blog model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Vues'),
        ),
    ]
