from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Person

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "petcad/index.html")

def login_view(request):
    if not request.method == "POST":
        return render(request, 'petcad/index.html')

    email    = request.POST.get("email")
    password = request.POST.get("password")

    if not email or not password:
        messages.error(request, "E-mail ou senha inválidos.")
        return render(request, 'petcad/index.html')
    
    try:
        # Busca a pessoa pelo e-mail no modelo Person
        person = Person.objects.get(email=email)
        user = person.user

        if user.check_password(password):
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, "Senha incorreta.")
            return render(request, 'petcad/index.html')
            
    except Person.DoesNotExist:
        messages.error(request, "E-mail não cadastrado.")
        return render(request, 'petcad/index.html')
 
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


def dashboard(request):
    email = request.user.email
    person = request.user.person_profile
    return render(request, "petcad/dashboard.html", {
        "person": person,
        "email": email
    })