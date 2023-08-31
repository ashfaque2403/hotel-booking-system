from django.contrib.auth.models import User
from django.db import models
import uuid
from phone_field import PhoneField

# Create your models here.


class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField( auto_now_add=True)

    class Meta:
        abstract=True

class Amenities(BaseModel):
    amenity_name=models.CharField(max_length=100)

    def __str__(self):
        return self.amenity_name

class Per(BaseModel):
    per_day=models.CharField(max_length=50)

    def __str__(self):
        return self.per_day

class Hotel(BaseModel):
    hotel_name=models.CharField(max_length=100)
    hotel_price=models.IntegerField()
    description=models.TextField()
    amenities=models.ManyToManyField(Amenities)
    room_count=models.IntegerField(default=10)
    per=models.ManyToManyField(Per)
    

    def __str__(self):
        return self.hotel_name

class HotelImages(BaseModel):
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='hotel_images')
    images=models.ImageField(upload_to='media')

    def __str__(self):
        return self.hotel.hotel_name

class HotelBooking(BaseModel):
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='hotel_booking')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_booking')
    start_date=models.DateField()
    end_date=models.DateField()
    phone =PhoneField(blank=True, help_text='Contact phone number')
    address=models.TextField(max_length=200)
    booking_type=models.CharField( max_length=100, choices=(('Pre Paid','Pre Paid'),('Post Paid','Post Paid')))

    def __str__(self):
        return f"{self.user.username}-{self.hotel.hotel_name}"
    