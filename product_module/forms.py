from django import forms

from product_module.models import ProductComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['product', 'parent', 'text']
