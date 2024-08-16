from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test





def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                
                login(request, user)
                if request.user.username == 'admin':
                    return redirect('index')

            
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})




def custom_logout(request):
    if request.method in ['POST', 'GET']: 
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))  # Redirect to login page after logout
    else:
        return HttpResponseRedirect(reverse_lazy('login'))
    




