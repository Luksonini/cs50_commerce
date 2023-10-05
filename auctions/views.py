from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListingModel, CategoryModel


def index(request):
    listing_from = ListingForm()
    rest_categories = CategoryModel.objects.all()
    auctions = AuctionListingModel.objects.all()
    watchlist_auctions = request.user.watchlist.all()
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
        

        elif request.POST["make_new_list"] == "True":    
            return render(request, "auctions/index.html", {
                "auctions" : auctions, 
                'watchlist_auctions' : watchlist_auctions, 
                "listing_from" : listing_from, 
                "rest_categories" : rest_categories, 
                "categories" : rest_categories
                })
    
    return render(request, "auctions/index.html", {
        "auctions" : auctions, 
        'watchlist_auctions' : watchlist_auctions, 
        "rest_categories" : rest_categories})


def category(request, category_id):
    listing_from = ListingForm()
    categories = CategoryModel.objects.get(pk=category_id)
    rest_categories = CategoryModel.objects.exclude(pk=category_id).all()
    auctions = categories.auctions.all()
    watchlist_auctions = request.user.watchlist.all()
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

        elif request.POST["make_new_list"] == "True":    
            return render(request, "auctions/index.html", {
                "auctions" : AuctionListingModel.objects.filter(auction_category=categories), 
                'watchlist_auctions' : watchlist_auctions, 
                "listing_from" : listing_from, 
                "rest_categories" : rest_categories,
                "categories" :  CategoryModel.objects.all(),
                "category_id" :  category_id
                })
    
    return render(request, "auctions/index.html", {
        "auctions" : auctions, 
        'watchlist_auctions' : watchlist_auctions, 
        "rest_categories" : rest_categories,
        "categories" : categories
        })

def login_view(request):
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
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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
        return render(request, "auctions/register.html")


from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label='Title',
        widget=forms.TextInput(attrs={'class': 'w-full rounded-lg'}),
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'w-full rounded-lg'}),
    )
    starting_bid = forms.FloatField(
        label='Starting Bid',
        widget=forms.NumberInput(attrs={'class': 'w-full rounded-lg'}),
    )
    image_url = forms.URLField(
        label='Image URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'w-full rounded-lg'}),
    )
    # category = forms.ModelMultipleChoiceField(queryset=CategoryModel.objects.all(),
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': "flex flex-wrap gap-5 form-checkbox h-5 w-5 text-indigo-600"}))

    def clean_starting_bid(self):
        starting_bid = self.cleaned_data.get('starting_bid')
        if starting_bid <= 0:
            raise forms.ValidationError('Starting bid must be a positive number.')
        return starting_bid
    

def create_listing(request):
    listing_from = ListingForm()
    categories = CategoryModel.objects.all()
    return render(request, "auctions/create_listing.html", {"listing_from" : listing_from, "categories" : categories})