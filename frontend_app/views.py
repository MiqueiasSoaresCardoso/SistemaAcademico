import requests
from django.conf import settings
from django.shortcuts import redirect, render


def api_request(request, method, endpoint, data=None):
    token = request.session.get('api_access_token')
    if not token:
        return {'status': 401, 'message': 'Token de acesso não encontrado'}

    headers = {'Authorization': f'Bearer {token}'}
    api_url = f'{settings.API_BASE_URL}{endpoint}'

    try:
        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, headers=headers, data=data)
        elif method == 'PUT':
            response = requests.put(api_url, headers=headers, data=data)
        elif method == 'PATCH':
            response = requests.patch(api_url, headers=headers, data=data)
        else:
            return {'status': 405, 'message': 'Método não suportado'}

        return {'status': response.status_code, 'data': response.json()}
    except requests.exceptions.RequestException:
        return {'status': 500, 'message': 'Erro de conexão'}



from django.conf import settings


import requests
from django.shortcuts import render, redirect
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        api_url = f"{settings.API_BASE_URL}auth/token/"

        try:
            response = requests.post(api_url, json={'email': email, 'password': password}, timeout=5)

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access')
                refresh_token = token_data.get('refresh')

                if not access_token or not refresh_token:
                    return render(request, 'login.html', {'error': 'Resposta inválida da API.'})

                # 🔑 salva tokens na sessão
                request.session['api_access_token'] = access_token
                request.session['api_refresh_token'] = refresh_token

                return redirect(reverse('dashboard'))

            elif response.status_code == 401:
                return render(request, 'login.html', {'error': 'Credenciais inválidas'})
            else:
                return render(request, 'login.html', {
                    'error': f'Erro na API ({response.status_code}): {response.text}'
                })

        except requests.exceptions.RequestException:
            return render(request, 'login.html', {'error': 'Erro de conexão com a API.'})

    return render(request, 'login.html')



def dashboard_view(request):
    token = request.session.get('api_access_token')
    headers = {'Authorization': f'Bearer {token}'}
    if not token:
        return redirect('login')

    try:
        cursos_url = f"{settings.API_BASE_URL}cursos/"
        cursos_response = requests.get(cursos_url, headers=headers)
        cursos_data = cursos_response.json()

        disciplinas_url = f"{settings.API_BASE_URL}disciplinas/"
        disciplinas_response = requests.get(disciplinas_url, headers=headers)
        disciplinas_data = disciplinas_response.json()

        context = {
            'cursos_total': cursos_data.get('count', 0),
            'disciplinas_total': disciplinas_data.get('count', 0),
        }
        return render(request, 'dashboard.html', context)

    except requests.exceptions.RequestException:
        return redirect('logout')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def perfis_list(request):
    response = api_request(request, 'GET', 'perfis/')
    if response['status'] in [401, 403]:
        return redirect('logout')
    context = {'perfis': response.get('data', {}).get('results', [])}
    return render(request, 'perfis/list.html', context)


def cursos_list(request):
    response = api_request(request, 'GET', 'cursos/')
    if response['status'] in [401, 403]:
        return redirect('logout')
    context = {'cursos': response.get('data', {}).get('results', [])}
    return render(request, 'cursos/list.html', context)


def disciplinas_list(request):
    response = api_request(request, 'GET', 'disciplinas/')
    if response['status'] in [401, 403]:
        return redirect('logout')
    context = {'disciplinas': response.get('data', {}).get('results', [])}
    return render(request, 'disciplinas/list.html', context)


def cursos_create(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = api_request(request, 'POST', 'cursos/', data)
        print(response)
        if response['status'] in [200, 201]:
            return redirect('cursos_list')
    return render(request, 'cursos/form.html')

def disciplina_create(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = api_request(request, 'POST', 'disciplinas/', data)
        print(response)
        if response['status'] in [200, 201]:
            return redirect('disciplinas_list')
    return render(request, 'disciplinas/form.html')