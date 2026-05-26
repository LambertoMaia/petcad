from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

from .models import Tutor, Animal, Vaccination
from .utils import filter_animals_by_species, build_vaccination_overview, get_species_emoji
from .forms import TutorForm, PetForm, VaccinationForm


def _selected_tutor_name(form):
    owner_id = None
    if form.is_bound and form.data.get('owner'):
        owner_id = form.data.get('owner')
    elif form.instance.pk and form.instance.owner_id:
        owner_id = form.instance.owner_id
    if owner_id:
        return Tutor.objects.filter(pk=owner_id).values_list('name', flat=True).first() or ''
    return ''


def _redirect_after_delete_error(request, fallback_name, **fallback_kwargs):
    next_url = request.POST.get('next', '').strip()
    if next_url.startswith('/') and not next_url.startswith('//'):
        return redirect(next_url)
    return redirect(fallback_name, **fallback_kwargs)


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'petcad/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method != 'POST':
        return render(request, 'petcad/index.html')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password')

    if not email or not password:
        messages.error(request, 'E-mail ou senha inválidos.')
        return render(request, 'petcad/index.html')

    candidates = User.objects.filter(
        Q(username__iexact=email) | Q(email__iexact=email)
    )
    user = None
    for candidate in candidates:
        user = authenticate(request, username=candidate.username, password=password)
        if user is not None:
            break

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

    tutor_count = Tutor.objects.count()
    pet_count = Animal.objects.count()
    dog_count = Animal.objects.filter(
        Q(species__icontains='cão') | Q(species__icontains='cao')
    ).count()
    cat_count = Animal.objects.filter(species__icontains='gato').count()
    dog_pct = round(dog_count / pet_count * 100) if pet_count else 0
    cat_pct = round(cat_count / pet_count * 100) if pet_count else 0

    recent_tutors = Tutor.objects.annotate(
        pet_count=Count('animals')
    ).order_by('-created_at')[:3]

    recent_pets = Animal.objects.select_related('owner').order_by('-created_at')[:3]

    return render(request, 'petcad/dashboard.html', {
        'admin_name': name,
        'tutor_count': tutor_count,
        'pet_count': pet_count,
        'dog_count': dog_count,
        'cat_count': cat_count,
        'dog_pct': dog_pct,
        'cat_pct': cat_pct,
        'recent_tutors': recent_tutors,
        'recent_pets': recent_pets,
    })

@login_required
def tutores(request):
    search = request.GET.get('q', '').strip()
    tutors = Tutor.objects.annotate(pet_count=Count('animals')).order_by('-created_at')
    if search:
        tutors = tutors.filter(name__icontains=search)
    return render(request, 'petcad/tutores.html', {
        'tutors': tutors,
        'search': search,
    })


@login_required
def novo_tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            tutor = form.save()
            messages.success(request, f'Tutor {tutor.name} cadastrado com sucesso.')
            return redirect('ver_tutor', pk=tutor.pk)
    else:
        form = TutorForm()
    return render(request, 'petcad/novo_tutor.html', {'form': form})


@login_required
def ver_tutor(request, pk):
    tutor = get_object_or_404(
        Tutor.objects.prefetch_related('animals'),
        pk=pk,
    )
    return render(request, 'petcad/ver_tutor.html', {'tutor': tutor})


@login_required
def editar_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados de {tutor.name} atualizados com sucesso.')
            return redirect('ver_tutor', pk=tutor.pk)
    else:
        form = TutorForm(instance=tutor)
    return render(request, 'petcad/editar_tutor.html', {'tutor': tutor, 'form': form})


@login_required
@require_POST
def excluir_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    password = request.POST.get('password', '')

    if not request.user.check_password(password):
        messages.error(request, 'Senha incorreta. Exclusão cancelada.')
        return _redirect_after_delete_error(request, 'ver_tutor', pk=pk)

    if tutor.animals.exists():
        messages.error(
            request,
            f'Não é possível excluir {tutor.name}. Remova os pets vinculados primeiro.',
        )
        return _redirect_after_delete_error(request, 'ver_tutor', pk=pk)

    name = tutor.name
    tutor.delete()
    messages.success(request, f'Tutor {name} excluído com sucesso.')
    return redirect('tutores')


@login_required
def todos_pets(request):
    species = request.GET.get('species', '')
    search = request.GET.get('q', '').strip()
    pets = Animal.objects.select_related('owner').order_by('-created_at')
    pets = filter_animals_by_species(pets, species)
    if search:
        pets = pets.filter(name__icontains=search)
    return render(request, 'petcad/todos_pets.html', {
        'active_species': species,
        'pets': pets,
        'search': search,
    })


@login_required
def novo_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            animal = form.save()
            messages.success(request, f'Pet {animal.name} cadastrado com sucesso.')
            return redirect('ver_pet', pk=animal.pk)
    else:
        form = PetForm()
    return render(request, 'petcad/novo_pet.html', {
        'form': form,
        'selected_tutor_name': _selected_tutor_name(form),
    })


@login_required
def ver_pet(request, pk):
    animal = get_object_or_404(
        Animal.objects.select_related('owner').prefetch_related('vaccinations'),
        pk=pk,
    )
    vaccination_rows, vaccination_counts = build_vaccination_overview(animal)
    return render(request, 'petcad/ver_pet.html', {
        'animal': animal,
        'vaccination_rows': vaccination_rows,
        'vaccination_counts': vaccination_counts,
        'species_emoji': get_species_emoji(animal.species),
    })


@login_required
def carteira_vacinas(request, pk):
    animal = get_object_or_404(
        Animal.objects.select_related('owner').prefetch_related('vaccinations'),
        pk=pk,
    )
    vaccinations = animal.vaccinations.all()
    return render(request, 'petcad/carteira_vacinas.html', {
        'animal': animal,
        'vaccinations': vaccinations,
        'species_emoji': get_species_emoji(animal.species),
    })


@login_required
def registrar_vacina(request, pk):
    animal = get_object_or_404(Animal.objects.select_related('owner'), pk=pk)
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.animal = animal
            vaccination.save()
            messages.success(request, f'Vacina {vaccination.name} registrada para {animal.name}.')
            return redirect('ver_pet', pk=animal.pk)
    else:
        form = VaccinationForm()
    return render(request, 'petcad/registrar_vacina.html', {
        'animal': animal,
        'form': form,
        'species_emoji': get_species_emoji(animal.species),
        'vaccine_suggestions': _vaccine_suggestions(animal),
    })


def _vaccine_suggestions(animal):
    from .utils import COMMON_VACCINES, get_species_group

    group = get_species_group(animal.species)
    if group:
        return COMMON_VACCINES[group]
    return ['Antirrábica', 'Polivalente V10', 'Gripe Canina', 'Giárdia']


@login_required
def editar_pet(request, pk):
    animal = get_object_or_404(Animal.objects.select_related('owner'), pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados de {animal.name} atualizados com sucesso.')
            return redirect('ver_pet', pk=animal.pk)
    else:
        form = PetForm(instance=animal)
    return render(request, 'petcad/editar_pet.html', {
        'animal': animal,
        'form': form,
        'selected_tutor_name': _selected_tutor_name(form),
    })


@login_required
@require_POST
def excluir_pet(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    password = request.POST.get('password', '')

    if not request.user.check_password(password):
        messages.error(request, 'Senha incorreta. Exclusão cancelada.')
        return _redirect_after_delete_error(request, 'ver_pet', pk=pk)

    name = animal.name
    animal.delete()
    messages.success(request, f'Pet {name} excluído com sucesso.')
    return redirect('todos_pets')
