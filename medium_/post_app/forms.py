from django import forms
from django.apps import apps

PostArticle = apps.get_model('post_app', 'PostArticle')
class CreateLoanForm(forms.ModelForm):
    closed = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = PostArticle
        fields = [
            'title',
            'description',
            'text',
        ]

    def __init__ (self, *args, **kwargs):
        profile = kwargs.pop("profile")
        super(CreateLoanForm, self).__init__(*args, **kwargs)
        self.fields["type"].queryset = LoanType.objects.filter(client_classes=profile.client_class)