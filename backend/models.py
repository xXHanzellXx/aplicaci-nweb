from datetime import datetime

# Estas clases son representaciones lógicas de tus colecciones en MongoDB
# Ayudan a visualizar qué datos necesita cada parte de la app.

class User:
    """Estructura para la colección 'users'"""
    # name: str
    # email: str
    # password: str (hashed)
    pass

class Clothe:
    """Estructura para la colección 'clothes' (El Catálogo)"""
    # name: str (Ej: "Camisa Vintage")
    # price: float
    # image: str (URL o ruta local como 'img/shirt1.png')
    # category: str ('top', 'bottom', 'accessory')
    pass

class Outfit:
    """Estructura para la colección 'outfits' (Lo que guarda el usuario)"""
    def __init__(self, user_id, shirt_img, pants_img):
        self.user_id = user_id
        self.shirt = shirt_img
        self.pants = pants_img
        self.saved_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "shirt": self.shirt,
            "pants": self.pants,
            "saved_at": self.saved_at
        }

class Rental:
    """Estructura para la colección 'rentals'"""
    # user_id: ObjectId
    # clothe_id: ObjectId
    # date: datetime
    pass