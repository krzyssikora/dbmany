from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinLengthValidator


POLISH = 1
SPANISH = 2
ENGLISH = 3
GERMAN = 4
CZECH = 5

LANGUAGE = [
    (POLISH, _('Polish')),
    (SPANISH, _("Spanish")),
    (ENGLISH, _('English')),
    (GERMAN, _('German')),
    (CZECH, _('Czech')),
]


class Group(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        'Person',
        through='Membership',
        # through_fields=('group', 'person')
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, "A name must be longer than just 1 character.")]
    )

    nationality = models.PositiveSmallIntegerField(
        choices=LANGUAGE,
        default=POLISH,
    )

    about = models.CharField(
        max_length=1000
    )
    groups = models.ManyToManyField(
        'Group',
        through='Membership',
        # through_fields=('group', 'person')
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    # spoken_languages =
    # todo https://pypi.org/project/django-multiselectfield/
    #  simple idea, but CSV, so commas not allowed in options (?)

    def __str__(self):
        return self.name

    def nationality_str(self):
        return LANGUAGE[self.nationality - 1][1]


class Membership(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        # related_name='Group'
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        # related_name='Person'
    )
    # inviter = models.ForeignKey(
    #     Person,
    #     on_delete=models.CASCADE,
    #     related_name="membership_invites",
    # )
    invite_reason = models.CharField(max_length=64)

    class Meta:
        unique_together = [['person', 'group']]
