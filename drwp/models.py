from django.db import models
from imagekit.models import ImageSpecField
from django.contrib.auth import get_user_model
from imagekit.processors import ResizeToFill, SmartResize
from django.db.models.signals import post_save
from django.db.models import Sum
from django.shortcuts import reverse

User = get_user_model()



# RESTAURANTS
COUNTRY = (
    ('GH', 'Ghana'),
    ('NG', 'Nigeria')
)

REGION = (
    ('Ashanti', 'Ashanti'),
    ('Bono_Region', 'Bono Region'),
    ('Bono_East_Region', 'Bono East Region'),
    ('Ahafo_Region', 'Ahafo Region'),
    ('Central', 'Central'),
    ('Eastern', 'Eastern'),
    ('Greater_Accra', 'Greater Accra'),
    ('Northern', 'Northern'),
    ('Savannah', 'Savannah'),
    ('North_East', 'North East'),
    ('Upper_East', 'Upper East'),
    ('Upper_West', 'Upper West'),
    ('Volta_Region', 'Volta Region'),
    ('Oti', 'Oti'),
    ('Western_Region', 'Western Region'),
    ('Western_North', 'Western North')
)

RESTAURANT_STATUS = (
    ('Online', 'Online'),
    ('Offline', 'Offline')
)

OFFLINE_REASON = (
    ('OUT_OF_MENU_HOURS', 'OUT_OF_MENU_HOURS'),
    ('INVISIBLE', 'INVISIBLE'),
    ('PAUSED_BY_USER', 'PAUSED_BY_USER'),
    ('PAUSED_BY_RESTAURANT', 'PAUSED_BY_RESTAURANT')
)

SERVICE_AVAILABILITY = (
    ('All-time', 'All-time'),
    ('Mornings', 'Mornings'),
    ('Afternoons', 'Afternoons'),
    ('Evenings', 'Evenings'),
)

MENU_TYPE = (
    ('MENU_TYPE_DELIVERY', 'Delivery'),
    ('MENU_TYPE_PICK_UP', 'Pickup')
)

ORDER_STATUS = (
    ('COOKING',"Cooking"),
    ('READY',"Ready"),
    ('ONTHEWAY',"On the way"),
    ('DELIVERED',"Delivered"),
)

PAYMENT_MODE = (
    ('CASH', 'Cash'),
    ('CARD', 'Card'),
    ('MOMO', 'Mobile Money')
)



class StoreCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'Store Categories'
        ordering = ['title']
        verbose_name_plural = "Store categories"

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.IntegerField()
    alt_contact = models.CharField(max_length=200, null=True, blank=True)
    category = models.ManyToManyField(StoreCategory, blank=True)
    store_image = models.ImageField(upload_to='store/raw')
    thumbnail = ImageSpecField(source='store_image', processors=[SmartResize(50, 50)], format='PNG')
    status = models.CharField(choices=RESTAURANT_STATUS, max_length=50)
    avg_prep_time = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100,  null=True, blank=True)
    city = models.CharField(max_length=500)
    street_name = models.CharField(max_length=100)
    region = models.CharField(choices=REGION, max_length=100)
    country = models.CharField(choices=COUNTRY, max_length=500)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    price = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='items/raw')
    #quantity = models.IntegerField(null=True, blank=True)
    suspended = models.BooleanField(default=False)
    tax_info = models.DecimalField(decimal_places=3, max_digits=20, null=True, blank=True)
    nutritional_info = models.TextField(null=True, blank=True)
    visible = models.BooleanField(default=True)
    product_info = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        db_table = 'Items'
        ordering = ['title']

    def __str__(self):
        return self.title

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500, null=True, blank=True)
    availability = models.CharField(choices=SERVICE_AVAILABILITY, max_length=100, blank=True, null=True)
    #categories = models.ManyToManyField(MenuCategory, blank=True)
    items = models.ManyToManyField(Item)
    class Meta:
        db_table = 'Menus'
        ordering = ['title']

    def __str__(self):
        return self.title



#CUSTOMERS
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return self.item.title
    class Meta:
        db_table = 'Order Items'
        ordering = ['item']



class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=50)
    items = models.ManyToManyField(OrderItem)
    drop_off_description = models.TextField()
    #subTotal = models.IntegerField()
    delivery_fee = models.IntegerField()
    grand_Total = models.IntegerField()
    paymentMode = models.CharField(choices=PAYMENT_MODE, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    ordered_on = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_on_the_way = models.BooleanField(default=False)
    is_cooking = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    class Meta:
        db_table = 'Order(Cart)'
        ordering = ['created_on']

