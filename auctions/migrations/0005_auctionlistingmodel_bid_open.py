# Generated by Django 4.2.1 on 2023-10-07 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_bidmodel_bid_date_alter_bidmodel_auction"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlistingmodel",
            name="bid_open",
            field=models.BooleanField(default=True),
        ),
    ]
