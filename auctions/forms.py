from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label='Title',
        widget=forms.TextInput(attrs={'class': 'w-full rounded-lg', 'placeholder': 'Enter the title of your listing here.'}),
        required=True,
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'w-full rounded-lg', 'placeholder': 'Enter the description of your listing in Markdown format. You can use Markdown syntax for formatting.'}),
        required=True,
    )
    starting_bid = forms.FloatField(
        label='Starting Bid',
        widget=forms.NumberInput(attrs={'class': 'w-full rounded-lg', 'placeholder': 'Enter the starting bid amount for your listing. Must be a positive number.'}),
        required=True,
    )
    image_url = forms.URLField(
        label='Image URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'w-full rounded-lg', 'placeholder': 'Optional: Provide a URL for the image related to your listing.'}),
    )

    def clean_starting_bid(self):
        starting_bid = self.cleaned_data.get('starting_bid')
        if starting_bid <= 0:
            raise forms.ValidationError('Starting bid must be a positive number.')
        return starting_bid

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 70, 'class': 'resize-none flex-1 border-none break-words outline-none mt-1 mb-1 bg-transparent'})) 


class BidForm(forms.Form):
    bid = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full pl-2 font-extrabold rounded-lg resize-none border-none break-words outline-none mt-1 mb-1 bg-transparent'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        initial_bid = kwargs.pop('initial_bid', None)
        super(BidForm, self).__init__(*args, **kwargs)

        if initial_bid is not None:
            self.fields['bid'].initial = initial_bid
            self.fields['bid'].min_value = initial_bid
    
    def clean_bid(self):
        cleaned_data = super(BidForm, self).clean()
        actual_bid = cleaned_data.get("bid")
        min_value = self.fields['bid'].min_value
        print(f"actual_bid : {actual_bid}, min value: {min_value}")

        if actual_bid is None:
            raise forms.ValidationError('Bid value is required.')

        if min_value is None:
            raise forms.ValidationError('There was an error with the minimum bid value. Please try again.')

        if actual_bid <= min_value:
            raise forms.ValidationError(f'Bid must be greater than current price: {min_value}$')

        return actual_bid
