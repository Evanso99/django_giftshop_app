from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib import messages
from .models import Cartitems, Product, Cart
from django.http import JsonResponse
import json
from django.shortcuts import  get_object_or_404
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.models import User
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomPasswordResetForm
from .models import CustomUser
from .forms import CustomUserUpdateForm
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import paypalrestsdk
from .models import Cart, ShippingAddress


def base(request):
    return render(request, 'base.html')
    

@login_required
def home(request):
    return render(request, 'home.html')



@login_required
def about(request):
    return render(request, 'about.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password, model=CustomUser)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login details. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.security_question = form.cleaned_data.get('security_question')
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            security_answer = form.cleaned_data['security_answer']
            User = get_user_model()
            try:
                user = User.objects.get(email=email, security_question=security_answer)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or security answer.')
                return redirect('password_reset')
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'new_password': new_password,
            })
            send_mail(subject, message, 'noreply@example.com', [user.email])
            messages.success(request, 'Your password has been reset. Please check your email for the new password.')
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})



def logout_view(request):
  
    response = render(request, 'base.html')

 
    clear_session_flag_script = """
    <script>
        // Clear the session flag
        sessionStorage.removeItem('loggedIn');
    </script>
    """
    response.content = (response.content.decode('utf-8') + clear_session_flag_script).encode('utf-8')

    return response





def contact_success_view(request):
    return render(request, 'contact_success.html')



@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Send email
        send_mail(
            f'New message from {name} ({email})',
            message,
            email,
            ['evansofficial054@gmail.com'],  
            fail_silently=False,
        )



@login_required
def shop(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, completed=False)
        cartitems = cart.cartitems_set.all()
        return render(request, 'shop.html', {'products': products, 'cart': cart})
    else:
        return render(request, 'shop.html', {'products': products})
    
    
def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'products': products})

def search_results(request):
    return render(request, 'search_results.html')




def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, completed=False)

    # Try to get the existing Cartitems object, or create it if it doesn't exist
    cartitem, created = Cartitems.objects.get_or_create(cart=cart, product=product)
    
    # Check if the cartitem was created or already existed
    if created:
        # If it was created, set the initial quantity to 1
        cartitem.quantity = 1
    else:
        # If it already existed, increment the quantity
        cartitem.quantity += 1

    cartitem.save()
    return redirect('cart')



def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user = user, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}
    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})



from .models import Cart, Cartitems, ShippingAddress

def checkout(request):
    user = request.user
    
    # get the user's cart and cart items
    cart, created = Cart.objects.get_or_create(user=user, completed=False)
    cartitems = cart.cartitems_set.all()
    
    # check if the cart is empty
    if not cartitems:
        return redirect('cart')
    
    # handle the shipping form submission
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        shipping_address = ShippingAddress.objects.create(user=user, cart=cart, address=address, city=city, state=state, zipcode=zipcode)
    
    # render the checkout page
    context = {
        'cart': cart,
        'cartitems': cartitems,
    }
    return render(request, 'checkout.html', context)


def updateCart(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    product = Product.objects.get(id=productId)
    user = request.user
    cart, created = Cart.objects.get_or_create(user = user, completed = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    if action == "add":
        cartitem.quantity += 1
        cartitem.save()
    

    return JsonResponse("Cart Updated", safe = False)


def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False) 

def product_detail(request):
    return render(request, 'product_detail')


@login_required
def my_view(request):
    user = User.objects.get(user=request.user)
    # do something with the user ob




@login_required
def payment(request):
    if request.method == 'POST':
        # Get the cart items and calculate the total amount
        cart_items = Cart.objects.filter(user=request.user, completed=False)
        if not cart_items:
            messages.error(request, 'No active cart found')
            return redirect('cart')
        cart = cart_items.first()
        total = sum(float(item.get_cart_total) for item in cart_items)

        # Check if cart is completed
        if cart.completed:
            messages.error(request, 'Cart already completed')
            return redirect('cart')

        # Convert the total to a string before passing it to the Payment object
        total_str = str(total)

        # Set up PayPal
        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET,
        })

        # Create a payment
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {'total': total_str, 'currency': 'USD'},
                'description': 'Payment for your order'
            }],
            'redirect_urls': {
                'return_url': 'http://example.com/complete-payment',
                'cancel_url': 'http://example.com/cancel-payment',
            },
        })

        if payment.create():
            # Save the payment ID and cart items in the session
            request.session['payment_id'] = payment.id
            request.session['cart_items'] = [item.id for item in cart_items]

            # Get the PayPal redirect URL and redirect the user
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    return redirect(redirect_url)
        else:
            messages.error(request, 'Failed to create PayPal payment')
            return redirect('cart')

    # If the request method is not POST,




def complete_payment(request):
    # Get the payment ID and cart items from the session
    payment_id = request.session.get('payment_id')
    cart_item_ids = request.session.get('cart_items')

    # Get the payer ID and execute the payment
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        # Update the cart items and mark the payment as complete
        cart_items = Cart.objects.filter(id__in=cart_item_ids)
        cart = Cart.objects.filter(cartitems__in=cart_items).first()
        if cart:
            for cart_item in cart_items:
                cart_item.completed = True
                cart_item.save()

            # Get the shipping details from the payment object
            shipping_address = payment.payer.payer_info.shipping_address
            address = shipping_address.line1
            city = shipping_address.city
            state = shipping_address.state
            zipcode = shipping_address.postal_code

            # Create a shipping address object
            shipping_address = ShippingAddress.objects.create(user=request.user, address=address, city=city, state=state, zipcode=zipcode, cart=cart)

            # Mark the cart as completed
            cart.completed = True
            cart.save()

        # Redirect the user to a confirmation page
        return redirect('confirmation')
    else:
        # Handle payment execution failure
        print('Error executing payment:', payment.error)
        return HttpResponse('Error executing payment')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Send email
        send_mail(
            f'New message from {name} ({email})',
            message,
            email,
            ['evansofficial054@gmail.com'],  # Replace with your actual email address
            fail_silently=False,
        )

        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


def payment_form(request):
    return render(request, 'payment_form.html')

def confirmation(request):
    return render(request, 'confirmation.html')

def account(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have been updated.')
            return redirect('account')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'account.html', {'form': form})





def password_reset_email(request):
    return render(request, 'password_reset_email.html')