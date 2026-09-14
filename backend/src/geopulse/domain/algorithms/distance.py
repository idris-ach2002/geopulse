import math

from geopulse.domain.models.location import Location


def haversine_distance_m(
    a: Location,
    b: Location,
) -> float:
    return _calculer_haversine_interne(
        a.latitude,
        a.longitude,
        b.latitude,
        b.longitude,
        Terre.RAYON_MOYEN,
    )


class Terre:
    """Regroupe les constantes physiques et géométriques de la Terre."""

    # Rayons (en mètres)
    RAYON_MOYEN: float = 6_371_000.0  # Utilisé pour Haversine
    RAYON_EQUATORIAL: float = 6_378_137.0  # Modèle WGS84
    RAYON_POLAIRE: float = 6_356_752.3  # Modèle WGS84

    # Géométrie & Dimensions
    CIRCONFERENCE_EQUATORIALE: float = 40_075_017.0
    APLATISSEMENT: float = 1 / 298.257223563
    MASSE: float = 5.972e24

    # Physique & Gravité
    GRAVITE_STANDARD: float = 9.80665
    VITESSE_LIBERATION: float = 11_186.0
    PERIODE_ROTATION: float = 86_164.1


def _calculer_haversine_interne(
    lat1: float, lon1: float, lat2: float, lon2: float, rayon: float
) -> float:
    """
    Le préfixe '_' indique qu'elle est masquée pour l'extérieur (privée).

    Important : math.sin, math.cos, etc. acceptent uniquement des radians.
    """
    l1, n1, l2, n2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = l2 - l1
    dlon = n2 - n1

    a = math.sin(dlat / 2) ** 2 + math.cos(l1) * math.cos(l2) * math.sin(dlon / 2) ** 2
    return 2 * math.asin(math.sqrt(a)) * rayon


def calculer_distance(a: Location, b: Location) -> tuple[float, float]:
    """
    Calcule la distance la plus courte le long d'un grand cercle entre
    points sur une sphère à partir de leurs coordonnées de latitude et de longitude

    La formule de Haversine telle quelle dans https://fr.wikipedia.org/wiki/Formule_de_haversine:

        La distance d entre deux points p1 et p2 (de latitudes θ₁ , θ₂ et
        de longitudes φ₁ , φ₂ en radians) se calcule ainsi :
        d = 2R x arcsin( √[ sin²((θ₂ - θ₁) / 2) + cos(θ₁) x cos(θ₂) x sin²((φ₂ - φ₁) / 2) ] )
        * R : Le rayon moyen de la Terre, fixé généralement à 6 371 km (ou 6 371 000 m).
        * d : La distance obtenue le long de la surface terrestre (arc de grand cercle).

    """
    metres = haversine_distance_m(a, b)
    return metres, metres / 1000
