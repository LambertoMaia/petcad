from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Tutor, Animal

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'petcad/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method != 'POST':
        return render(request, 'petcad/index.html')

    email = request.POST.get('email')
    password = request.POST.get('password')

    if not email or not password:
        messages.error(request, 'E-mail ou senha inválidos.')
        return render(request, 'petcad/index.html')

    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return redirect('dashboard')

    messages.error(request, 'E-mail ou senha incorretos.')
    return render(request, 'petcad/index.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    name = request.user.get_full_name() or request.user.first_name or request.user.username
    return render(request, 'petcad/dashboard.html', {
        'admin_name': name,
    })

@login_required
def tutores(request):
    return render(request, 'petcad/tutores.html')


@login_required
def novo_tutor(request):
    return render(request, 'petcad/novo_tutor.html')


@login_required
def ver_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    return render(request, 'petcad/ver_tutor.html', {'tutor': tutor})


@login_required
def editar_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    return render(request, 'petcad/editar_tutor.html', {'tutor': tutor})


@login_required
@require_POST
def excluir_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if tutor.animals.exists():
        messages.error(
            request,
            f'Não é possível excluir {tutor.name}. Remova os pets vinculados primeiro.',
        )
        return redirect('tutores')
    tutor.delete()
    messages.success(request, f'Tutor {tutor.name} excluído com sucesso.')
    return redirect('tutores')


@login_required
def todos_pets(request):
    species = request.GET.get('species', '')
    return render(request, 'petcad/todos_pets.html', {'active_species': species})


@login_required
def novo_pet(request):
    return render(request, 'petcad/novo_pet.html')


@login_required
def ver_pet(request, pk):
    animal = get_object_or_404(Animal.objects.select_related('owner'), pk=pk)
    return render(request, 'petcad/ver_pet.html', {'animal': animal})


@login_required
def editar_pet(request, pk):
    animal = get_object_or_404(Animal.objects.select_related('owner'), pk=pk)
    return render(request, 'petcad/editar_pet.html', {'animal': animal})


@login_required
@require_POST
def excluir_pet(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    name = animal.name
    animal.delete()
    messages.success(request, f'Pet {name} excluído com sucesso.')
    return redirect('todos_pets')
