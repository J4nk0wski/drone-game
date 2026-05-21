from shared import GameObject, CollisionSide, CollisionInfo
from shared import Vector2
from drone import Drone

"""
Sprawdz czy wystąpiła kolizja i oblicza dane kolizji CollisionInfo
"""
def check_collision(dynamic: GameObject, static: GameObject) -> CollisionInfo:
    if not dynamic.rect.colliderect(static.rect):
        return CollisionInfo(False, CollisionSide.NONE, None, None)

    d_rect = dynamic.rect
    s_rect = static.rect
    
    overlaps = {
        CollisionSide.TOP: d_rect.bottom - s_rect.top,
        CollisionSide.BOTTOM: s_rect.bottom - d_rect.top,
        CollisionSide.LEFT: d_rect.right - s_rect.left,
        CollisionSide.RIGHT: s_rect.right - d_rect.left,
    }
    side = min(overlaps, key=overlaps.get)
    if isinstance(dynamic, Drone):
        return CollisionInfo(True, side, static, dynamic.velocity)
    return CollisionInfo(True, side, static, None)
