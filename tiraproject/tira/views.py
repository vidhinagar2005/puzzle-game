from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Brand,Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
# Create your views here.


# payments/views.py
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# # from django.shortcuts import render, redirect
# from django.http import JsonResponse, HttpResponseBadRequest
# from .models import Payment

# def initiate_payment(request):
#     if request.method == "POST":
#         amount = int(request.POST.get("amount")) * 100  # Convert to paise
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         payment_data = {
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": "1"
#         }
#         order = client.order.create(payment_data)

#         payment = Payment.objects.create(
#             order_id=order["id"],
#             amount=amount / 100  # Store in rupees
#         )

#         context = {
#             "order_id": order["id"],
#             "amount": amount,
#             "razorpay_key_id": settings.RAZORPAY_KEY_ID,
#             "callback_url": "/payments/callback/"
#         }
#         return render(request, "payments/payment_page.html", context)
#     return render(request, "payments/initiate_payment.html")


# @csrf_exempt
# def payment_callback(request):
#     if request.method == "POST":
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         data = request.POST

#         try:
#             params_dict = {
#                 'razorpay_order_id': data.get('razorpay_order_id'),
#                 'razorpay_payment_id': data.get('razorpay_payment_id'),
#                 'razorpay_signature': data.get('razorpay_signature')
#             }

#             # Verify the payment signature
#             client.utility.verify_payment_signature(params_dict)

#             payment = Payment.objects.get(order_id=params_dict['razorpay_order_id'])
#             payment.payment_id = params_dict['razorpay_payment_id']
#             payment.status = "paid"
#             payment.save()

#             return render(request, "payments/payment_success.html", {"payment": payment})
#         except Exception as e:
#             print(e)
#             return render(request, "payments/payment_failed.html")
#     return HttpResponseBadRequest()





# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request):
    data = json.loads(request.body)
    amount = int(data.get('amount', 0))
    order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })
    return JsonResponse(order)













def home(request):
    return render(request,'home.html')

# def makeup(request):
#     return render(request,'makeup.html')

def category(request, name):
    categories = Category.objects.all()
    category = Category.objects.get(name=name)
    print(category)
    products = category.product_set.all()
    print(products)
    brand = Brand.objects.all()
    return render(request, 'makeup.html', {'categories': categories,'products': products, 'brands': brand,'name': category})

def singal_product(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    # releted product
    related_product = Product.objects.filter(category=product.category)[:8]
    brand = Brand.objects.all()
    return render(request, 'single_product.html', {'categories': categories, 'brands': brand, 'products': product, 'related_products': related_product})

@login_required
def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart = request.session.get('cart',{})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1

    else:
        cart[str(product_id)] = {
            "name" : product.name,
            "price" : product.price,
            "quantity" : 1,
            "img" : product.img.url if product.img else None,

        }

        request.session['cart'] = cart
        request.session.modify = True
    return redirect("cart_view")
    
def cart_view(request):
    categories = Category.objects.all()
    brand = Brand.objects.all()
    cart = request.session.get("cart",{})
    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request,'cart.html',{'categories' : categories, 'total_amount' : total_amount, 'brand' : brand, 'cart':cart})

def update_cart(request, product_id, action):
    cart = request.session.get("cart", {})
    
    if str(product_id) in cart:
        if action == "increase":
            cart[str(product_id)]['quantity'] += 1
        elif action == "decrease":
            if cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1
            else:
                del cart[str(product_id)]
                
    request.session['cart'] = cart
    request.session.modified = True
    return redirect("cart_view")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect("cart_view")





def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        messages.success(request,'Account created successfully! Please log in.')
        # return redirect(login_user)
        return redirect(cart_view)
    
    return render(request,'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            return redirect('/') 
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('register')

    return render(request, "login.html")

def account(request):
    return render(request,'account.html',{'user' : request.user})

def logout_user(request):
    logout(request)
    return redirect('/')


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishcart = request.session.get('wishcart', {})
    
    # if str(product_id) in cart:
    #     cart[str(product_id)]['quantity'] += 1
    # else:
    wishcart[str(product_id)] = {
        "name" : product.name,
        "price" : product.price,

        "quantity" : 1,
        "image" : product.img.url if product.img else None, 
        }
    
    request.session['wishcart'] = wishcart
    request.session.modified = True
    print(wishcart)
    return redirect("wishlist_view")

def wishlist_view(request):
    categories = Category.objects.all()
    brand = Brand.objects.all()
    wishcart = request.session.get("wishcart", {})
    print(wishcart)
    # total_amount = sum(item['price'] * item['quantity'] for item in request.session.get('cart', {}).values())
    total_amount = sum(witem['price'] * witem['quantity'] for witem in wishcart.values())
    return render(request, 'wishlist.html', {'categories': categories, 'total_amount': total_amount,'brands': brand, 'cart': wishcart})  

def remove_from_wishlist(request, product_id):
    cart = request.session.get("wishcart", {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['wishcart'] = cart
        request.session.modified = True
        
    return redirect("wishlist_view")