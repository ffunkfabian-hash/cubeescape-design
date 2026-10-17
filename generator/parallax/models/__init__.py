"""Ten ordered, individually authored fictional low-poly weapon concepts."""
from . import pistol, assault, impulse, shotgun, sniper, smg, fusion, trace, rocket, bow

MODULES=(pistol,assault,impulse,shotgun,sniper,smg,fusion,trace,rocket,bow)


def load_all():
    """Return each model's metadata together with a fresh independent assembly."""
    return [(module.META.copy(),module.build()) for module in MODULES]
