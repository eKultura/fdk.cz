from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0028_alter_projectrolepermission_permission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LawDocument',
            fields=[
                ('document_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('document_type', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'FDK_law_document',
            },
        ),
    ]
