from django.db import models

# Create your models here.


class DepartmentBudget(models.Model):
    department_name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    available_budget = models.DecimalField(max_digits=10, decimal_places=2)

  

    def _str_(self):
        return self.department_name

class Invoice(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        # Add more departments as needed
    ]
    INVOICE_TYPES = [
        ('Hardware and Infrastructure', 'Hardware and Infrastructure'),
        ('Software and Licensing Fees', 'Software and Licensing Fees'),
        ('Support and Training', 'Support and Training'),
        ('Advertising and Media Buying', 'Advertising and Media Buying'),
        ('Promotional Activities', 'Promotional Activities'),
        ('Training and Development', 'Training and Development'),
        ('Travel and Transportation', 'Travel and Transportation'),
        ('Digital Sales Resources', 'Digital Sales Resources'),
        ('Equipment and Supplies', 'Equipment and Supplies'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    invoice_number = models.CharField(max_length=100)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    vat = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    invoice_image = models.ImageField(upload_to='invoices/')
    invoice_type = models.CharField(max_length=100, choices=INVOICE_TYPES)

    def _str_(self):
        return self.invoice_number
    
class DepartmentDescription(models.Model):
    department = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.department    