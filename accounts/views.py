import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class EmailVerificationView(View):
    def get(self, request, email):
        return render(request, 'accounts/verify_email.html', {'email': email})
    
    def post(self, request, email):
        user = CustomUser.objects.get(email=email)
        verification_code = request.POST.get('verification_code')
        if verification_code == user.verification_code:
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Email verified successfully!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid verification code.')
            return render(request, 'accounts/verify_email.html', {'email': email})


class UserRegistrationView(View):

    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        full_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password_confirm = request.POST.get('re_pass')

        if password == password_confirm:
            try:
                user = CustomUser.objects.create_user(
                    first_name=full_name.split()[0],
                    last_name=full_name.split()[1] if len(full_name.split()) > 1 else '',
                    email=email,
                    password=password,
                    username=username,
                    verification_code=str(random.randint(100000, 999999)),
                    is_active=False,  # Set to False until email verification
                )
                user.save()
                user = CustomUser.objects.get(email=email)
                verification_code = user.verification_code
                subject = 'Your Verification Code'
                message = f'Your verification code is: {verification_code}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                print(f"Sending email from {from_email} to {email} with code {verification_code}")
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.add_message(request, messages.SUCCESS, 'Verification email sent!')
            except:
                messages.add_message(request, messages.ERROR, 'Something went wrong.')
                return render(request, 'accounts/register.html')
            messages.add_message(request, messages.SUCCESS, 'Registration successful!')
            return redirect('verify_email', email=email)
        else:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

class UserLoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Login successful!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password.')
            return render(request, 'accounts/login.html')
        
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successful!')
        return redirect('home')