# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages():

    images = transport.getAllImages()  

    cards = []

    for imagen in images:
        card = translator.fromRequestIntoCard(imagen)
        cards.append(card)

    return cards


    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """
    
def filterByCharacter(name):
    all_cards = getAllImages()
    filtered = [card for card in all_cards if name.lower() in card.name.lower()]
    return filtered
    """
    Filtra las cards de personajes según el nombre proporcionado.
    
    Se debe filtrar los personajes cuyo nombre contenga el parámetro recibido. Retorna una lista de Cards filtradas.
    """
    pass

def filterByStatus(status_name):
    all_cards = getAllImages()  # trae todas las cards
    return [card for card in all_cards if card.status == status_name]

   
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """
    pass

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    if request.user.is_authenticated and request.method == "POST":
        # Convertimos los datos del POST en una Card
        card = translator.fromRequestIntoCard(request.POST)
        card.user = request.user  # asignamos el usuario actual
        repositories.saveFavourite(card)  # lo guardamos en la DB
    """
    Guarda un favorito en la base de datos.
    
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    pass

def getAllFavourites(request):
    if request.user.is_authenticated:
        user = request.user
        # Traemos todos los favoritos desde el repositorio
        favourites = repositories.getAllFavourites(user)
        # Convertimos los favoritos en Cards para enviar al template
        cards = [translator.fromDBToCard(fav) for fav in favourites]
        return cards
    else:
        return []
    """
    Obtiene todos los favoritos del usuario autenticado.
    
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    pass

def deleteFavourite(request):
     if request.user.is_authenticated and request.method == "POST":
        favourite_id = request.POST.get("id")
        repositories.deleteFavourite(favourite_id)  # elimina usando el ID
