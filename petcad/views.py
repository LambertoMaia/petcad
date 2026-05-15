from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'petcad/index.html')


def login_view(request):
    if not request.method == "POST":
        messages.error(request, "Não foi possível efetuar o login")
        return render(request, 'petcad/index.html')

    email       = request.POST.get("email")
    password    = request.POST.get("password")

    if not email and not password:
        messages.error(request, "E-mail ou senha inválidos.")
        return render(request, 'petcad/index.html')
    
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return redirect('dashboard') 
    else:
        messages.error(request, "E-mail ou senha inválidos.")
        return render(request, 'petcad/index.html')


from .models import Person # Add this import

def register_view(request):
    if not request.method == "POST":
        return render(request, 'petcad/index.html')
    
    full_name = request.POST.get("full_name")
    email     = request.POST.get("email")
    password  = request.POST.get("password")
    cpf       = request.POST.get("cpf")
    telephone = request.POST.get("telephone")
    address   = request.POST.get("address")

    if not all([full_name, email, password, cpf, telephone, address]):
        messages.error(request, "Verifique se todos os campos foram preenchidos corretamente.")
        return render(request, 'petcad/index.html')

    if User.objects.filter(username=email).exists():
        messages.error(request, "Este e-mail já está cadastrado.")
        return render(request, 'petcad/index.html')

    # 1. Criar o usuário Auth
    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = full_name
    user.save()

    # 2. Criar o perfil Person vinculado
    Person.objects.create(
        user=user,
        name=full_name,
        email=email,
        cpf=cpf,
        telephone=telephone,
        address=address
    )

    messages.success(request, "Sua conta foi criada com sucesso! Agora você pode fazer o login.")
    return redirect('index')

    
