from django import forms
from django.shortcuts import get_object_or_404

from . import models
from authentication import models as auth

RATING_CHOICES = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
]


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES, label='Note :')

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre :', 'body': 'commentaire :'}


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserFollowsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        set request user in user
        """
        self.user = kwargs.pop(
            'request_user')
        super(UserFollowsForm, self).__init__(*args, **kwargs)

    followed_user = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}), label="s'abonner"
    )

    class Meta:
        model = models.UserFollows
        fields = ["followed_user", "user"]
        exclude = ["user"]

    def clean_followed_user(self):
        """
        check if the user exist and get the user object correspondent to the text input
        """
        username = self.cleaned_data.get("followed_user", None)
        users = auth.User.objects.all()
        if username == str(self.user):
            raise forms.ValidationError("Vous ne pouvez pas vous follow")
        elif str(username) not in [str(user.username) for user in users]:
            raise forms.ValidationError("Cet utilisateur n'existe pas")
        else:
            followed_user = get_object_or_404(auth.User, username=username)
        return followed_user

    def save(self, commit=True):
        follow = models.UserFollows(
            user=self.user,
            followed_user=self.clean_followed_user()
        )
        if commit:
            follow.save()
        return follow


class DeleteUserFollowsForm(forms.Form):
    delete_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)
