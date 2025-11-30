
from django.urls import path
from .views import get_note, CustomTokenObtainPairView, CustomRefreshTokenView, logout, is_auth, register

urlpatterns = [
    
    path('login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),

    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    
    # path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('notes/', get_note),
    path('logout/', logout),
    path('is_auth/', is_auth),
    path('register/', register)
    
]