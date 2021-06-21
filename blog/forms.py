from django import forms

from .models import Comment, Post, Tag

from django.contrib.auth.forms import UserCreationForm, UsernameField


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', )

        widgets = {

            'author': forms.Select(attrs={
                'class': 'form-control mb-1',
            }),

            'title': forms.TextInput(attrs={
                'class': 'form-control mb-1',
            }),

            'excerpt': forms.TextInput(attrs={
                'class': 'form-control mb-1'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control mb-1',
                'rows': '5'
            }),

            'tags': forms.widgets.SelectMultiple(attrs={
                'class': 'form-control'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control mb-1'
            })
        }

        help_texts = {
            'tags': 'You can choose multiple tags'
        }


class CommentForm(forms.Form):
    username = forms.CharField(
        max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    text = forms.CharField(max_length=320, widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError('Text must be at least 10 characters')
        return text


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('username', 'email', 'text')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your username...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your email...'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What do you think ?'}),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError('Text must be at least 10 characters')
        return text

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not '@test.com' in email:
            raise forms.ValidationError(
                'Invalid email address, must endwith \'@test.com\'')
        return email
