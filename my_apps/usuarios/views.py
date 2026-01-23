from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, Group
from django.contrib import messages

from my_apps.usuarios.models import Membership, Organization, Profile
from django.contrib.auth.models import User


def loginView(request):

    if request.user.is_authenticated:
        return redirect('portafolios:projects')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, f'Bienvenido {user.username}')

            next_url = request.GET.get('next')
            return redirect(next_url or 'portafolios:projects')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html', {
        'form': form
    })

def registerView(request):
    
    if request.user.is_authenticated:
        return redirect('portafolios:projects')
    
    form = UserCreationForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Te has registrado correctamente')
        return redirect('portafolios:projects')
    
    
    return render(request, './register.html', {
        'form': form
    })



def logoutView(request):
    logout(request)
    return redirect('portafolios:projects')



@login_required
def profileView(request):
    
    profile = User.objects.get(id=request.user.id).profile
    
    
    context = {
        'profile': profile
    }

    return render(request, 'profile/profile.html', context)


def OrganizationView(request):
    return redirect('portafolios:under_construction')



def MemeberShipView(request):
    return redirect('portafolios:under_construction')



# @login_required
# def create_user_with_group(request):

#     if not request.user.is_staff:
#         messages.error(
#             request,
#             '❌ No tienes permisos para realizar esta acción'
#         )
#         return redirect('portafolios:projects')

#     form = UserCreationForm(request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = True
#         user.save()

#         # 👉 Asignar grupo
#         group_name = 'creadores'  # ejemplo
#         group, created = Group.objects.get_or_create(name=group_name)
#         user.groups.add(group)

#         messages.success(
#             request,
#             f'Usuario "{user.username}" creado y asignado al grupo "{group_name}"'
#         )

#         return redirect('portafolios:projects')

#     return render(request, 'register.html', {
#         'form': form
#     })