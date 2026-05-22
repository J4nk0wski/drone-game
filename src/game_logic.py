from shared import GameObject, CollisionSide, CollisionInfo

"""
Sprawdz czy wystąpiła kolizja i oblicza dane kolizji CollisionInfo
"""
def check_collision(dynamic: GameObject, static: GameObject) -> CollisionInfo:
    d_rect = dynamic.rect
    s_rect = static.rect

    if not d_rect.colliderect(s_rect):
        return CollisionInfo(False, CollisionSide.NONE, None, None)

    overlaps = {
        CollisionSide.TOP: d_rect.bottom - s_rect.top,
        CollisionSide.BOTTOM: s_rect.bottom - d_rect.top,
        CollisionSide.LEFT: d_rect.right - s_rect.left,
        CollisionSide.RIGHT: s_rect.right - d_rect.left,
    }
    side = min(overlaps, key=overlaps.get)
    velocity_to_return = getattr(dynamic, 'velocity', None)

    return CollisionInfo(True, side, static, velocity_to_return)
