from django.urls import path
from app_document.views.index_view import IndexView
from app_document.views.pricing_view import PricingView
from app_document.views.manual_view import ManualView

app_name = 'app_document'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('manual/', ManualView.as_view(), name='manual'),

]