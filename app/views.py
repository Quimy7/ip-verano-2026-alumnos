# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'login.html')


def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    
    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    """
    images = services.getAllImages()
    favourite_list=[]
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    if request.method == "POST":
        query = request.POST.get('query', '').strip()

        # Si no se ingresó nada, volver a home
        if not query:
            return redirect('home')

        # Filtrar imágenes por nombre
        images = services.filterByCharacter(query)

        # Lista de favoritos (si después la querés completar con DB)
        favourite_list = []

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    # Para cualquier otro método (GET, PUT, etc.), redirigir a home
    return redirect('home')

    """
    Busca personajes por nombre.
    
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    pass

def filter_by_status(request):
    if request.method == "POST":
        status = request.POST.get('status', '').strip()  # Alive o Deceased
        if not status:
            return redirect('home')

        images = services.filterByStatus(status)

        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
        else:
            favourite_list = []

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')
    


    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    pass

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourites = services.getAllFavourites(request)
    return render(request, 'favoritos.html', {'favourite_list': favourites})
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    pass

@login_required
def saveFavourite(request):
    if request.method == "POST":
        card = services.fromRequestToCard(request.POST)  # convierte los datos en Card
        card.user = request.user
        services.saveFavourite(card)
    return redirect('home')
    """
    Guarda un personaje como favorito.
    """
    pass

@login_required
def deleteFavourite(request):
    if request.method == "POST":
        favourite_id = request.POST.get('id')
        services.deleteFavourite(favourite_id)
    return redirect('favoritos')  # redirige a la página de favoritos
    """
    Elimina un favorito del usuario.
    """
    pass


@login_required
def exit(request):
    logout(request)
    return redirect('home')