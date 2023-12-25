# Generated by Django 5.0 on 2023-12-25 11:51

import django.db.models.deletion
import food_recipes_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Category|name')),
                ('description', models.TextField(blank=True, verbose_name='Category|description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ingredient|name')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Unit|name')),
                ('name_abbrev', models.CharField(blank=True, max_length=60, verbose_name='Unit|name_abbrev')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Recipe|name')),
                ('description', models.TextField(verbose_name='Recipe|description')),
                ('difficulty', models.SmallIntegerField(choices=[(1, 'Difficulty|easy'), (2, 'Difficulty|medium'), (3, 'Difficulty|hard')], default=2, verbose_name='Recipe|difficulty')),
                ('cooking_steps', models.TextField(verbose_name='Recipe|cooking_steps')),
                ('cooking_duration', models.DurationField(verbose_name='Recipe|cooking_duration')),
                ('dish_img', models.ImageField(blank=True, upload_to=food_recipes_app.models.gen_name, verbose_name='Recipe|dish_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Recipe|author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_recipes_app.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Quantity')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_recipes_app.ingredient', verbose_name='Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_recipes_app.recipe')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='food_recipes_app.RecipeIngredient', to='food_recipes_app.ingredient', verbose_name='Ingredients'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measure_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_recipes_app.unit', verbose_name='Unit'),
        ),
    ]
