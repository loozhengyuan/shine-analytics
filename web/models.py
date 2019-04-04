from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code


class CustomerAccount(models.Model):
    code = models.CharField(max_length=255, unique=True)
    postal = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'customer account'
        verbose_name_plural = 'customer accounts'

    def __str__(self):
        return self.code


class SalesPerson(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'salesperson'
        verbose_name_plural = 'salespersons'

    def __str__(self):
        return self.code


class Project(models.Model):
    code = models.CharField(max_length=255, unique=True)
    custaccount = models.ForeignKey(CustomerAccount, on_delete=models.SET_NULL, null=True)
    salesperson = models.ForeignKey(SalesPerson, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.code


class Document(models.Model):
    date = models.DateField(max_length=255)
    reference = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'

    def __str__(self):
        return self.reference


class Location(models.Model):
    code = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __str__(self):
        return self.code


class Transaction(models.Model):
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    transacted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        unique_together = (("document", "project"),)

    def __str__(self):
        return "{self.document} {self.project}".format(self=self)
