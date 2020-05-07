from django import forms
from .models import Comment, Post


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True, label='Sujet')
    message = forms.CharField(widget=forms.Textarea, required=True)


class SearchForm(forms.Form):
	question = forms.CharField(max_length=50)

	def __str__(self):
		return self.question



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class PostCreationForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'summary', 'content', 'picture', 'category', 'tags',)
