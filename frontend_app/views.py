import requests
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            api_url = f"{settings.API_BASE_URL}auth/token"
            response = requests.post(api_url,data={'email':email, 'password':password})
            if response.status_code == 200:
                token_data = response.json()
                request.session['api_acess_token'] = token_data['access']
                return redirect('dashboard')
            else:
                return render(request,'login.html',{'error': 'Credenciais invalidas'})

        except requests.exceptions.RequestException:
            return render(request,'login.html',{'error': 'Erro de conexão com a API.'})

    return render(request,'login.html')

