# capa DAO de acceso/persistencia de datos.
from app.models import Favourite

def saveFavourite(fav):
    fav = Favourite.objects.create(
        name=fav.name,
        gender=fav.gender,
        status=fav.status,
        occupation=fav.occupation,
        phrases=fav.phrases,
        age=fav.age,
        image=fav.image,
        user=fav.user
    )
    return fav

def getAllFavourites(user):
    """
    Obtiene todos los favoritos de un usuario desde la base de datos.
    """
    pass

def deleteFavourite(favId):
    favourite = Favourite.objects.get(id=favId)
    favourite.delete()
    return True