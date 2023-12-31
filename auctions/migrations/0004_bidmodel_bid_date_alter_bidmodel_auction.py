# Generated by Django 4.2.1 on 2023-10-06 20:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_commentmodel_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="bidmodel",
            name="bid_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bidmodel",
            name="auction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.auctionlistingmodel",
            ),
        ),
    ]
