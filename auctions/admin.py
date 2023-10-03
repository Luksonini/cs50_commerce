from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionListingModel, CategoryModel, BidModel, CommentModel

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')  # Wyświetlane pola w panelu administratora
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Pola, po których można wyszukiwać użytkowników


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('auction_name', 'initial_bid', 'actual_bid', 'owner', 'picture', 'created_at')
    search_fields = ('auction_name', 'owner__username')  # Dla wyszukiwania po nazwie aukcji i nazwie właściciela
    filter_horizontal = ('auction_category',)
    filter_horizontal = ('watch_list',)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'comment')  # Wyświetlane pola w panelu admina
    list_filter = ('auction', 'commenter')  # Filtry do filtrowania komentarzy
    search_fields = ('auction__auction_name', 'commenter__username')  # Wyszukiwanie po nazwie aukcji i nazwie komentującego
    filter_horizontal = ('auction',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(AuctionListingModel, AuctionListingAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(CategoryModel)
admin.site.register(BidModel)
