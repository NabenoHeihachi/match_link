from django.urls import path
from app_profile.views.profile_personality_view import ProfilePersonalityView
from app_profile.views.profile_profile_view import ProfileProfileView
from app_profile.views.profile_setup_view import ProfileSetupView

app_name = 'app_profile'

urlpatterns = [
    path('personality/', ProfilePersonalityView.as_view(), name='personality'),
    path('profile/', ProfileProfileView.as_view(), name='profile'),
    path('setup/', ProfileSetupView.as_view(), name='setup'),
]
