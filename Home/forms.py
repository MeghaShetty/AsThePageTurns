from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile,Book,PersonalCollection,Chapter,Forum,Thread

class UserForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={'invalid': _("This value must contain only letters,"
                                                                                  " numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                                label=_("Confirm Password"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
            if len(self.cleaned_data['password1']) < 8:
                raise forms.ValidationError(_("The password is too short."))
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserProfileForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea)
    blog = forms.URLField(max_length=100)
    coverpic = forms.ImageField(label='Select a cover image')
    profilepic = forms.ImageField(label='Select a profile image')

    class Meta:
        model = UserProfile
        fields = {'about','blog','coverpic','profilepic'}


class ChapterForm(forms.ModelForm):
    chapter_title = forms.CharField(max_length=20)
    chapter_content = forms.CharField(max_length=3000,widget=forms.Textarea)

    class Meta:
        model = Chapter
        fields = ['chapter_no','chapter_title','chapter_content']