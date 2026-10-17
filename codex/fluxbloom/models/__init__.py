"""Original model collection for K · Flux Bloom, independently built by Codex."""
from . import pistol, assault, impulse, shotgun, sniper, smg, fusion, trace, rocket, bow
MODULES = (pistol, assault, impulse, shotgun, sniper, smg, fusion, trace, rocket, bow)


def load_all():
    return [(dict(module.META), module.build()) for module in MODULES]
