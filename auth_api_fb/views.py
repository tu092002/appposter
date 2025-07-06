from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"success": False, "message": "Sai tài khoản hoặc mật khẩu."}, status=401)

    if not user.is_active:
        return Response({"success": False, "message": "Tài khoản đã bị khóa."}, status=403)

    if user.expiry_date and user.expiry_date < date.today():
        return Response({"success": False, "message": "Tài khoản đã hết hạn."}, status=403)

    # 🔒 Kiểm tra đã đăng nhập ở nơi khác chưa
    if cache.get(f"user_logged_in:{username}"):
        return Response({"success": False, "message": "Tài khoản đã đăng nhập ở nơi khác."}, status=403)

    # ✅ Cho phép đăng nhập, tạo token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # ✅ Lưu trạng thái đã login
    cache.set(f"user_logged_in:{username}", {
        "logged_in": True,
        "timestamp": str(datetime.now())
    }, timeout=86400)

    return Response({
        "success": True,
        "message": "Đăng nhập thành công.",
        "username": user.username,
        "expiry_date": user.expiry_date,
        "token": access_token,
        "refresh": refresh_token,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    username = request.user.username
    cache.delete(f"user_logged_in:{username}")
    return Response({"message": "Đã đăng xuất thành công."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({"success": False, "message": "Vui lòng nhập đầy đủ mật khẩu cũ và mới."}, status=400)

    if not user.check_password(old_password):
        return Response({"success": False, "message": "Mật khẩu cũ không chính xác."}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"success": True, "message": "Đổi mật khẩu thành công."})
