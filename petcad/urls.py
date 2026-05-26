from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/login', views.login_view, name='user_login'),
    path('user/logout', views.logout_view, name='user_logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('tutores/', views.tutores, name='tutores'),
    path('tutores/novo/', views.novo_tutor, name='novo_tutor'),
    path('tutores/<int:pk>/', views.ver_tutor, name='ver_tutor'),
    path('tutores/<int:pk>/editar/', views.editar_tutor, name='editar_tutor'),
    path('tutores/<int:pk>/excluir/', views.excluir_tutor, name='excluir_tutor'),
    path('pets/', views.todos_pets, name='todos_pets'),
    path('pets/novo/', views.novo_pet, name='novo_pet'),
    path('pets/<int:pk>/', views.ver_pet, name='ver_pet'),
    path('pets/<int:pk>/vacinas/', views.carteira_vacinas, name='carteira_vacinas'),
    path('pets/<int:pk>/vacinas/nova/', views.registrar_vacina, name='registrar_vacina'),
    path('pets/<int:pk>/editar/', views.editar_pet, name='editar_pet'),
    path('pets/<int:pk>/excluir/', views.excluir_pet, name='excluir_pet'),
]
