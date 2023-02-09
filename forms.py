from django import forms
from dbmany.models import Person, Group
from django.core.files.uploadedfile import InMemoryUploadedFile
from ads.humanize import naturalsize


# Create the form class.
class CreatePersonForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'
    groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all(),
        # empty_label=None
    )
    # invite_reason = forms.CharField(required=False, max_length=64)

    class Meta:
        model = Person
        fields = [
            'name',
            'about',
            'nationality',
            'groups',
            'picture'
        ]  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreatePersonForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateGroupForm, self).save(commit=False)

        if commit:
            instance.save()

        return instance

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
