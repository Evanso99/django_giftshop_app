from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from . import views



urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name="search"),
    path('search_results/', views.search_results, name='search_results'),
    path('logout/', views.logout_view, name='logout_view'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("updatecart", views.updateCart, name="updateCart"),
    path('updatequantity', views.updateQuantity, name='updatequantity'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('payment/', views.payment, name='payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('complete-payment/', views.complete_payment, name='complete_payment'),
    path('account/', views.account, name='account'),
    
    path('password_reset_email/', views.password_reset_email, name='password_reset_email'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
