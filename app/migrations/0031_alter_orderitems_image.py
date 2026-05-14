# Generated manually for deployment: store product image URL in order line items.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_alter_order_tracking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='image',
            field=models.CharField(max_length=512),
        ),
    ]
