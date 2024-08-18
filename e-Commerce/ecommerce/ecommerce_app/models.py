from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(max_length=500)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=50)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='shop/images')

    def __str__(self):
        return self.product_name
