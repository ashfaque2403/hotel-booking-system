from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .models import Amenities,Hotel,HotelBooking,Per,HotelImages
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from datetime import datetime
# Create your views

@login_required(login_url='login')
def index(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.order_by('-created_at')
    per=Per.objects.all()
    
    search = request.GET.get('search')
    amenities = request.GET.getlist('amentities')  # Update the parameter name here to 'amentities'

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains=search) |
            Q(description__icontains=search)|
            Q(hotel_price__icontains=search)
        )

    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in=amenities)
        
    context = {
        'amenities_objs': amenities_objs,
        'hotels_objs': hotels_objs,
        'per': per,
        'search': search,
        'amentities': amenities,  # Update the variable name here to 'amenities'
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request,'account not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user_obj=authenticate(username=username, password=password)
        if not user_obj:
            messages.warning(request,'invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        login(request,user_obj)    
        return redirect('/')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'login.html')

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)

        if user_obj.exists():
            messages.warning(request,'already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user=User.objects.create(username=username,email=email,password=password)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'register.html')

def check_booking(start_date, end_date, uid, room_count):
    overlapping_qs = HotelBooking.objects.filter(
        Q(start_date__lte=start_date, end_date__gte=start_date) |  
        Q(start_date__lte=end_date, end_date__gte=end_date) |      
        Q(start_date__gte=start_date, end_date__lte=end_date),     
        hotel__uid=uid
    )

    if len(overlapping_qs) >= room_count  :  
        return False
    return True
   
@login_required(login_url='login')
def rooms(request,uid):
    hotels_objs=Hotel.objects.get(uid=uid)

    if request.method=='POST':
        checkin=request.POST.get('checkin')
        checkout=request.POST.get('checkout')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        hotel=Hotel.objects.get(uid=uid)

        today = datetime.now().date()
        start_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        end_date = datetime.strptime(checkout, '%Y-%m-%d').date()

        if start_date < today or end_date < today:
            messages.warning(request, 'Unknown Error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

      
        if not check_booking(checkin,checkout,uid,hotel.room_count):
            messages.warning(request,'hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel,user=request.user,start_date=checkin,end_date=checkout,
        booking_type='Check in',phone=phone,address=address)

        messages.success(request,'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    context = {
        'hotels_objs': hotels_objs,
        
    }
    return render(request,'rooms.html',context)

def adminpage(request):
    adminbook=HotelBooking.objects.order_by('-created_at')
    hotels_objs=Hotel.objects.all()
    users = User.objects.all()
    context={
        'adminbook':adminbook,
        'hotels_objs':hotels_objs,
        'users':users,
    }

    return render(request,'adminpage.html',context)

def logout_view(request):
    logout(request)
  # Redirect to a success page.
    return redirect('index')

def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def profile(request):
    booked=HotelBooking.objects.filter(user=request.user)
    

    context={
        'booked':booked,
        # 'hotels_objs':hotels_objs,

    }
    return render(request,'profile.html',context) 

def delete(request, uid):
    bookings = HotelBooking.objects.filter(uid=uid)
    bookings.delete()
    messages.success(request,'your booking has been cancelled')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def payment(request):
    return render(request,'payment.html')