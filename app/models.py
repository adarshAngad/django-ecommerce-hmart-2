from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.timezone import datetime
# Create your models here.
import uuid

class Categories(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name
	
class Brand(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Color(models.Model):
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Filter_Price(models.Model):
	FILTER_PRICE = (
		('1000 To 3000', '1000 To 3000'),
		('3000 To 6000', '3000 To 6000'),
		('6000 To 9000', '6000 To 9000'),
		('9000 To 11000', '9000 To 11000'),
		('11000 To 20000', '11000 To 20000'),
		('20000 To 40000', '20000 To 40000'),
	)
	price = models.CharField(choices=FILTER_PRICE,max_length=60)
	def __str__(self):
		return self.price
	
class Product(models.Model):
	CONDITION = (('New','New'),('Old','Old'))
	STOCK = ('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK')
	STATUS = ('Publish','Publish'),('Draft','Draft')

	unique_id = models.CharField(unique=True,max_length=200,null=True,blank=True)
	image = models.ImageField(upload_to='Product_images/img')
	name = models.CharField(max_length=200)
	price = models.CharField(max_length=100)
	condition = models.CharField(choices=CONDITION,max_length=100)
	information = RichTextField(null=True)
	description = RichTextField(null=True)
	stock = models.CharField(choices=STOCK,max_length=200)
	discount = models.CharField(max_length=50,null=True,blank=True)
	status = models.CharField(choices=STATUS,max_length=200)
	created_date = models.DateTimeField(default=timezone.now)

	categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
	brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
	color = models.ForeignKey(Color,on_delete=models.CASCADE)
	filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE)


	def save(self,*args,**kwargs):
		if self.unique_id is None and self.created_date and self.id:
			self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
		return super().save(*args,**kwargs)
	
	def __str__(self):
		return self.name
	
class Images(models.Model):
	image = models.ImageField(upload_to='Product_images/img')
	product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Tag(models.Model):
	name = models.CharField(max_length=200)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Contact_us(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Ordered', 'Ordered'),
        ('Shipping', 'Order Shipping'),
        ('Way', 'On the Way'),
        ('Completed', 'Order Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField()
    additional_info = models.TextField(blank=True)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=300, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(default=datetime.today)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Ordered', null=True)
    tracking_id = models.CharField(max_length=20,default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.user.username



class OrderItems(models.Model):
    # Choices for order status
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.CharField(max_length=512)
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.order.user.username} - {self.product}"