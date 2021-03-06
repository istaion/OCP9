# Generated by Django 4.0.3 on 2022-04-20 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_user_follows'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.review')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='contributors',
            field=models.ManyToManyField(related_name='contributions', through='review.TicketContributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticketcontributor',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.ticket'),
        ),
        migrations.AlterUniqueTogether(
            name='ticketcontributor',
            unique_together={('contributor', 'ticket')},
        ),
    ]
