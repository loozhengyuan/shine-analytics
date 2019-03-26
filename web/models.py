from django.db import models

# Create your models here.
class Document(models.Model):
    date = models.DateField(max_length=255)
    reference = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'

    def __str__(self):
        return ("{self.date} {self.reference}").format(self=self)


class Customer(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    postal = models.IntegerField()
    contact = models.IntegerField()

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return ("{self.code} {self.name}").format(self=self)


class Currency(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'

    def __str__(self):
        return ("{self.code} {self.description}").format(self=self)


class Project(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return ("{self.code} {self.description}").format(self=self)


class Location(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __str__(self):
        return ("{self.code} {self.description}").format(self=self)


class SalesPerson(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    contact = models.IntegerField()

    class Meta:
        verbose_name = 'salesperson'
        verbose_name_plural = 'salespersons'

    def __str__(self):
        return ("{self.code} {self.name}").format(self=self)


class Transaction(models.Model):
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    salesperson = models.ForeignKey(SalesPerson, on_delete=models.SET_NULL, null=True)
    transacted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        unique_together = (("document", "customer", "project"),)

    def __str__(self):
        return ("{self.document} {self.customer} {self.project}").format(self=self)
