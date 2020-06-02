from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.document = kwargs.pop('document', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.document = self.document
        comment.save()

    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Input your comments'})
        }
        labels = {
            'body': ''
        }