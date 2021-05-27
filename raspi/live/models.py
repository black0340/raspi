from django.db import models

# Create your models here.
class SavedImage(models.Model):
    UltraSonic = models.IntegerField()
    ImageNumber = models.IntegerField()
    CreatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()