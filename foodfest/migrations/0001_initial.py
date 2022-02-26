# Generated by Django 4.0.1 on 2022-02-01 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(default='', max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('desc', models.CharField(max_length=300)),
                ('image', models.ImageField(default='', upload_to='food/images')),
            ],
        ),
        migrations.CreateModel(
            name='PersonDetails',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=200)),
                ('postal', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPost',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]