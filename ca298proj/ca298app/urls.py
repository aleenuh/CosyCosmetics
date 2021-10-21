from django.urls import path, include
from . import views
from .forms import UserLoginForm
from .models import CaUser, Product
from rest_framework import routers, serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CaUser
        fields = ['url', 'username', 'email', 'is_staff']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('allproducts/', views.all_products, name='all_products'),
    path('product/<int:prodid>', views.singleproduct, name='product_single'),
    path('add/', views.addproducts),
    path('register/', views.CaUserSignupView.as_view(), name='register'),
    path('admins/', views.AdminSignupView.as_view(), name='Admin register'),
    path('Login/', views.Login.as_view(template_name='login.html', authentication_form=UserLoginForm), name='Login'),
    path('Logout/', views.logout_view, name='logout'),
    path('addbasket/<int:prodid>', views.add_to_basket, name='add_to_basket'),
    path('api/', include(router.urls))
]

