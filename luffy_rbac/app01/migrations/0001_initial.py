# Generated by Django 4.0.4 on 2022-05-28 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.CharField(max_length=32, verbose_name='年龄')),
                ('email', models.EmailField(max_length=32, verbose_name='邮箱')),
                ('company', models.CharField(max_length=32, verbose_name='公司')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(verbose_name='付费金额')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='付费时间')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.customer', verbose_name='关联客户')),
            ],
        ),
    ]
