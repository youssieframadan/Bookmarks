from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey('auth.User',related_name='actions',db_index=True,on_delete=models.CASCADE)
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_object',on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,blank=True)
    target = GenericForeignKey('target_ct','target_id')
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)