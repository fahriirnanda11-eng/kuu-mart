import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail



def register_user(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registrasi berhasil. Silakan login."
        )

        return redirect('login')

    return render(request, 'register.html')


def login_user(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:

            authenticated_user = authenticate(
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                # Membuat OTP 6 digit
                otp = str(random.randint(100000, 999999))

                # Simpan data sementara di session
                request.session['otp'] = otp
                request.session['otp_user_id'] = user.id

                # Kirim OTP
                send_mail(
                    'Kode OTP Login KUU Mart',
                    f'Kode OTP kamu adalah: {otp}',
                    None,
                    [user.email],
                    fail_silently=False,
                )

                return redirect('verify_otp')

        messages.error(
            request,
            "Email atau password salah."
        )

    return render(request, 'login.html')


def verify_otp(request):

    if 'otp' not in request.session:
        messages.error(
            request,
            "Silakan login terlebih dahulu."
        )
        return redirect('login')

    if request.method == "POST":

        otp_input = request.POST['otp']

        otp_session = request.session.get('otp')
        user_id = request.session.get('otp_user_id')

        if otp_input == otp_session:

            try:
                user = User.objects.get(id=user_id)

                login(request, user)

                # Hapus OTP setelah berhasil
                del request.session['otp']
                del request.session['otp_user_id']

                messages.success(
                    request,
                    "Login berhasil. Selamat datang di KUU Mart!"
                )

                return redirect('/')

            except User.DoesNotExist:
                messages.error(
                    request,
                    "Akun tidak ditemukan."
                )

        else:
            messages.error(
                request,
                "Kode OTP salah."

            )

    return render(request, 'verify_otp.html')


def logout_user(request):

    logout(request)

    return redirect('/')