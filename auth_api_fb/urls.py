from django.urls import path
from .views import login_view, logout_view, change_password_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),  # ✅ Cho phép logout rõ ràng
    path('change-password/', change_password_view, name='change_password'),  # ✅ mới thêm


]
