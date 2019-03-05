from django.db import models

# Create your models here.
class AccountsReceivable(models.Model):
    docdate = models.CharField(max_length=255)
    docref = models.CharField(max_length=255)
    actcode = models.CharField(max_length=255)
    cusname = models.CharField(max_length=255)
    postcode = models.IntegerField()
    custel = models.IntegerField()
    actcur = models.CharField(max_length=3)
    actcurwtax = models.DecimalField(max_digits=15, decimal_places=2)
    homecurwtax = models.DecimalField(max_digits=15, decimal_places=2)
    projcode = models.CharField(max_length=255)
    location = models.IntegerField()
    salescode = models.CharField(max_length=255)
    salesname = models.CharField(max_length=255)
    salestel = models.IntegerField()

    class Meta:
        verbose_name = 'accounts receivable'
        verbose_name_plural = 'accounts receivables'

    def __str__(self):
        return self.docdate, self.docref, self.actcode