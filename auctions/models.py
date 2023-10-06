from django.contrib.auth.models import AbstractUser
from django.db import models


from django.db import models

class User(AbstractUser):
    """
    Custom user model representing a user of the auction platform.
    """
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class CategoryModel(models.Model):
    """
    Model representing categories for auctions.
    """
    category = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.category


class AuctionListingModel(models.Model):
    """
    Model representing an auction listing.
    """
    auction_name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    initial_bid = models.IntegerField()
    actual_bid = models.IntegerField(blank=True, null=True, default=None)
    auction_category = models.ManyToManyField(CategoryModel, related_name='auctions')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_auctions')
    watch_list = models.ManyToManyField(User, related_name='watchlist')
    picture = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auction: {self.auction_name} Owner: {self.owner} Current price: {self.actual_bid}"


class BidModel(models.Model):
    """
    Model representing bids on auction listings.
    """
    auction = models.ForeignKey(AuctionListingModel, on_delete=models.CASCADE, related_name="auctions")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()

    def __str__(self):
        return f"Auction: {self.auction.auction_name} Bidder: {self.bidder} Bid Amount: {self.bid_amount}"


class CommentModel(models.Model):
    """
    Model representing comments on auction listings.
    """
    auction = models.ManyToManyField(AuctionListingModel, related_name="comments_for_auction")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        first_auction = self.auction.first()
        auction_name = first_auction.auction_name if first_auction else "Unknown"
        return f"Auction: {auction_name} Commenter: {self.commenter} Comment: {self.comment}"