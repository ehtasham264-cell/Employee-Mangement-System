from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0003_employee_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
