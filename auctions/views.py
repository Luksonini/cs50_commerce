from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown
from .models import User, AuctionListingModel, CategoryModel, BidModel, CommentModel
from . forms import ListingForm, CommentForm, BidForm
from django.contrib.auth.decorators import login_required


def index(request):
    """
    Display the main auction listings page. 
    Users can view all available auctions and add/remove items from their watchlist.
    """
    rest_categories = CategoryModel.objects.all()
    auctions = AuctionListingModel.objects.exclude(bid_open=False).all()
    if request.user.is_authenticated:
        watchlist_auctions = request.user.watchlist.all()
    else:
        watchlist_auctions = None
    for auction in auctions:
        if not auction.actual_bid:
            auction.actual_bid = auction.initial_bid
            auction.save()
    if request.method == "POST":

        add_to_watchlist = request.POST.get("add_to_wathlist")
        remove_from_watchlist = request.POST.get("remove_from_watchlist")
        if add_to_watchlist:
            auction_id = int(add_to_watchlist)
            auction_to_add = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.add(auction_to_add)

        elif remove_from_watchlist:
            auction_id = int(remove_from_watchlist)
            auction_to_remove = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.remove(auction_to_remove)
    
    return render(request, "auctions/index.html", {
        "auctions" : auctions, 
        'watchlist_auctions' : watchlist_auctions, 
        "rest_categories" : rest_categories})

@login_required
def watchlist(request):
    """
    Display the watchlist page for the authenticated user. 
    Users can view all the auctions they have added to their watchlist and can also add/remove items.
    """
    rest_categories = CategoryModel.objects.all()
    auctions = request.user.watchlist.all()
    if request.user.is_authenticated:
        watchlist_auctions = request.user.watchlist.all()
    else:
        watchlist_auctions = None
    for auction in auctions:
        if not auction.actual_bid:
            auction.actual_bid = auction.initial_bid
            auction.save()
    if request.method == "POST":

        add_to_watchlist = request.POST.get("add_to_wathlist")
        remove_from_watchlist = request.POST.get("remove_from_watchlist")
        if add_to_watchlist:
            auction_id = int(add_to_watchlist)
            auction_to_add = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.add(auction_to_add)

        elif remove_from_watchlist:
            auction_id = int(remove_from_watchlist)
            auction_to_remove = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.remove(auction_to_remove)
            auctions = request.user.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "auctions" : auctions, 
        'watchlist_auctions' : watchlist_auctions, 
        "rest_categories" : rest_categories})


def category(request, category_id):
    """
    Display all the auctions associated with a particular category.
    Users can view all auctions under a category and can add/remove items from their watchlist.
    """
    categories = CategoryModel.objects.get(pk=category_id)
    rest_categories = CategoryModel.objects.exclude(pk=category_id).all()
    auctions = categories.auctions.all()
    if request.user.is_authenticated:
        watchlist_auctions = request.user.watchlist.all()
    else:
        watchlist_auctions = None
    if request.method == "POST":

        add_to_watchlist = request.POST.get("add_to_wathlist")
        remove_from_watchlist = request.POST.get("remove_from_watchlist")
        if add_to_watchlist:
            auction_id = int(add_to_watchlist)
            auction_to_add = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.add(auction_to_add)

        elif remove_from_watchlist:
            auction_id = int(remove_from_watchlist)
            auction_to_remove = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.remove(auction_to_remove)
    
    return render(request, "auctions/index.html", {
        "auctions" : auctions, 
        'watchlist_auctions' : watchlist_auctions, 
        "rest_categories" : rest_categories,
        "categories" : categories
        })



def login_view(request):
    """
    Handle user login. If the POST method is used, attempt to authenticate the user. 
    If successful, redirect them to the main page. If not, display an error message.
    """
    rest_categories = CategoryModel.objects.all()
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {"rest_categories" : rest_categories})


def logout_view(request):
    """
    Log the user out and redirect them to the login page.
    """
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    """
    Handle user registration. If the POST method is used, attempt to create a new user account.
    If successful, log the user in and redirect them to the main page.
    """
    rest_categories = CategoryModel.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {"rest_categories" : rest_categories})

@login_required
def create_listing(request):
    """
    Allow users to create a new auction listing. 
    Users can provide details for the auction, select categories, and submit the form to create the auction.
    """
    listing_from = ListingForm()
    categories = CategoryModel.objects.exclude(category__in=["Open", "Closed"]).all()

    if request.method == "POST":
        listing_from = ListingForm(request.POST)
        if listing_from.is_valid():
            title = listing_from.cleaned_data['title']
            description = listing_from.cleaned_data['description']
            starting_bid = listing_from.cleaned_data['starting_bid']
            image_url = listing_from.cleaned_data.get('image_url')
            categories = request.POST.getlist('categories')
           
            new_auction = AuctionListingModel(
                    auction_name=title,
                    description=description,
                    initial_bid=starting_bid,
                    actual_bid = starting_bid,
                    picture=image_url,
                    owner=request.user)
            
            new_auction.save()

            for category in categories:
                category_to_add = CategoryModel.objects.get(pk=category)
                new_auction.auction_category.add(category_to_add)
            new_auction.auction_category.add(CategoryModel.objects.get(category="Open"))
            new_auction.auction_category.remove(CategoryModel.objects.get(category="Closed"))

            return redirect('index')

    return render(request, "auctions/create_listing.html", {"listing_from" : listing_from, "categories" : categories, "rest_categories" : categories})


def details(request, auction_id):
    """
    Display detailed view of a particular auction. 
    Users can view all the details, add/remove the auction from watchlist, place a bid, add comments, and owners can close the bid.
    """
    auction = AuctionListingModel.objects.get(pk=auction_id)
    description = markdown.markdown(auction.description)
    rest_categories = CategoryModel.objects.all()
    # comments = auction.comments_for_auction.all()
    comments = auction.comments_for_auction.all().order_by('-created_at')
    bids = auction.bids.all().order_by('-bid_amount')
    initial_bid = bids.first().bid_amount if bids else auction.initial_bid  # handles case where there are no bids yet
    bid_form = BidForm(initial_bid=initial_bid)
    comment_form = CommentForm()

    if request.method == 'POST':

        add_to_watchlist = request.POST.get("add_to_wathlist")
        remove_from_watchlist = request.POST.get("remove_from_watchlist")
        if add_to_watchlist:
            auction_id = int(add_to_watchlist)
            auction_to_add = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.add(auction_to_add)

        elif remove_from_watchlist:
            auction_id = int(remove_from_watchlist)
            auction_to_remove = AuctionListingModel.objects.get(pk=auction_id)
            request.user.watchlist.remove(auction_to_remove)

        if 'bid' in request.POST:  
            bid_form = BidForm(request.POST, initial_bid=initial_bid)
            if bid_form.is_valid():
                bid_value = bid_form.cleaned_data['bid']
                if bid_value > initial_bid:
                    new_bid = BidModel.objects.create(auction=auction, bidder=request.user, bid_amount=bid_value)
                    auction.actual_bid = bid_value
                    auction.save()
                    new_bid.save()
                    bids = auction.bids.all().order_by('-bid_amount')

        if 'comment' in request.POST:  
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.cleaned_data['comment']
                last_comment = auction.comments_for_auction.last()
                if not last_comment or last_comment.comment != comment:
                    new_comment = CommentModel.objects.create(commenter=request.user, comment=comment)
                    new_comment.auction.add(auction)
                    # comments = auction.comments_for_auction.all()  
                    comments = auction.comments_for_auction.all().order_by('-created_at') # reload the comments
   
        if 'close_bid' in request.POST and request.user == auction.owner:
            category = CategoryModel.objects.get(category="Closed")
            auction.auction_category.add(category)
            auction.bid_open = False
            auction.auction_category.remove(CategoryModel.objects.get(category="Open"))
            auction.save()

    return render(request, "auctions/details.html", {
        "auction": auction,
        "comments": comments,
        "comment_form": comment_form,
        "bids": bids,
        'description': description,
        "bid_form": bid_form,
        "rest_categories" : rest_categories
    })