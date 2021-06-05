"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appstore.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('cancelado/', CanceladoView.as_view(), name='cancelado'),
    # path('sucesso/', SucessoView.as_view(), name='sucesso'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('', index.as_view(), name='index'),
    path('base/', base, name='base'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

]
