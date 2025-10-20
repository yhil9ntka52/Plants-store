from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    registration_date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

class Plant(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    detailed_description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    care_type = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='created')
    creation_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
