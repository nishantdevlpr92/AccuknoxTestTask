from django.db import models

from .constants import FRIEND_TYPE, PENDING

class Friends(models.Model):

    sender = models.ForeignKey(
        "account.user", related_name="sender", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "account.user", related_name="receiver", on_delete=models.CASCADE
    )
    status = models.CharField(choices=FRIEND_TYPE, max_length=40, default=PENDING)
    created_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
