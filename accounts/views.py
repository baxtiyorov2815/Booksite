from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


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
                    is_active=True,
                )
                user.save()
            except:
                messages.add_message(request, messages.ERROR, 'Something went wrong.')
                return render(request, 'accounts/register.html')
            messages.add_message(request, messages.SUCCESS, 'Registration successful!')
            return redirect('login')
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