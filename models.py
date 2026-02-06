
from django.db import models

class Bookmark(models.Model):
    username = models.CharField(max_length=150,default='unknown_user')
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

