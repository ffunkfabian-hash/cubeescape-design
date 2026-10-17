"""Independent, hand-relative design reference, not a validated importer contract.

Raw faces and ``bounding_box`` retain the renderer's model coordinates. Every
``*_m`` geometry field uses the documented right-handed Blender reference frame.
No geometry is changed or rescaled by this exporter.
"""
from copy import deepcopy
import numpy as np
from eng import bounds

M = np.array([[0., 0., 1.], [-1., 0., 0.], [0., -1., 0.]])
CHANNELS = ('MT_Primary', 'MT_Secondary', 'MT_Accent', 'MT_Metal',
            'MT_Energy', 'MT_Emission', 'MT_Detail')
REFERENCE_SOURCE = ('claude/docs/weapon-spec.md, Achsen und Maßstab; '
                    'Toolgen-0.13-Weltmodellmessung vom 17.10.2026')
FIT_SOURCE = ('claude/docs/weapon-spec.md, Größe in der Roboterhand; '
              'Cube Escape 0.82, Docs/EQUIPMENT.md, Stand 17.10.2026')
LENGTHS_M = dict(pistol=.243, assault=.934, impulse=.862, shotgun=.904,
                 sniper=1.134, smg=.616, fusion=.960, trace=1.044, rocket=.725, bow=1.018)
FIT_LENGTHS_M = dict(assault=.67, impulse=.66, shotgun=.67, sniper=.73,
                    smg=.52, fusion=.67, trace=.69, rocket=.65)
SIGHT_TYPES = {
    'standard': ('reflex', 'glass'), 'holo': ('holo', 'glass'),
    'precision': ('scope', 'lens'), 'reflex': ('reflex', 'glass'),
    'sniper': ('scope', 'lens'), 'machine': ('reflex', 'glass'),
    'energy': ('energy', 'glass'), 'trace': ('holo', 'glass'),
    'rocket': ('holo', 'glass'), 'iron': ('iron', 'none'), 'pin': ('pin', 'open'),
}


# Metadata for our own renderer recipes, provided by the skin author. These are
# descriptive ingredients, not a promise that a downstream tool can bake them.
SKIN_DETAILS = {
    'circuit_bloom': (['cross_part_blocks', 'paired_diagonal_bands', 'original_segment_number_07', 'physical_ribs'], ['paint', 'metal']),
    'tidal_pulse': (['longitudinal_gradient', 'concentric_rings', 'original_segment_number_18', 'physical_ribs'], ['paint', 'metal']),
    'gilt_vector': (['gold_cross_part_block', 'chrome_band', 'original_segment_number_03', 'physical_ribs', 'edge_wear'], ['paint', 'gold', 'chrome']),
    'transit_mark': (['cross_part_warning_bands', 'dark_front_block', 'original_segment_number_23', 'physical_ribs'], ['paint', 'metal']),
    'chrome_crest': (['cross_part_chrome_blocks', 'copper_band', 'original_segment_number_08', 'physical_fins', 'edge_wear'], ['paint', 'chrome', 'metal']),
}


def _vec(value):
    return np.asarray(value, dtype=float).round(9).tolist()


def _box(part):
    return bounds([part])


def _center(part):
    lo, hi = _box(part)
    return (lo + hi) / 2


def _channel(part):
    declared = getattr(part, 'channel', None)
    if declared is not None:
        if declared not in CHANNELS:
            raise ValueError(f'Unknown material channel: {declared}')
        return declared, 'explicit: part.channel'
    from skins import channel_for
    return channel_for(part), 'inferred: skins.channel_for material/role fallback'


def _surface_area(part):
    # Newell's area vector handles concave planar polygons without fan overcount.
    return sum(float(np.linalg.norm(np.sum(np.cross(f.vertices, np.roll(f.vertices, -1, axis=0)), axis=0))) / 2
               for f in part.faces)


def _anchor_candidates(model, labels, sight=False):
    return [i for i, p in enumerate(model) if p.sight == sight and not getattr(p, 'skin_trim', False)
            and (p.label or '').casefold() in labels]


def _anchors(meta, model):
    """Return model coordinates first; metre positions are added after origin selection."""
    result = {}
    def set_anchor(key, index=None, point=None, source='', reason=None):
        result[key] = dict(model=None if point is None else _vec(point),
                           part=None if index is None else f'p{index:03d}',
                           source=source, null_reason=reason)
    grip = _anchor_candidates(model, {'griff', 'pistolengriff', 'griffstück', 'bogengriff'})
    triggers = _anchor_candidates(model, {'abzug'})
    if grip:
        # Pick the grip closest behind the trigger when several are named.
        trigger_x = _center(model[triggers[0]])[0] if triggers else float('inf')
        grip.sort(key=lambda i: (_center(model[i])[0] > trigger_x,
                                 abs(_center(model[i])[0] - trigger_x) if triggers else i))
        i = grip[0]
        set_anchor('Socket_Hand', i, _center(model[i]), 'inferred: named grip bounding-box centre')
    else:
        set_anchor('Socket_Hand', source='unavailable', reason='No named primary grip or explicit hand anchor.')
    origin = result['Socket_Hand']['model']
    hand_x = origin[0] if origin else float('-inf')
    support = _anchor_candidates(model, {'vordergriff', 'pumpgriff', 'pumpmanschette', 'stützgriff',
                                         'handschutz', 'laufverkleidung', 'laufmantel', 'laufhülle'})
    support = [i for i in support if _center(model[i])[0] > hand_x]
    if support:
        i = max(support, key=lambda j: np.prod(_box(model[j])[1] - _box(model[j])[0]))
        set_anchor('Socket_SupportHand', i, _center(model[i]), 'inferred: named forward grip/handguard bounding-box centre')
    else:
        set_anchor('Socket_SupportHand', source='unavailable', reason='No named forward grip/handguard; no cup grip guessed.')
    muzzle = _anchor_candidates(model, {'pfeilspitze'}) if meta['slug'] == 'bow' else []
    if not muzzle:
        muzzle = _anchor_candidates(model, {'mündung', 'zweite mündung', 'lauf', 'emitter', 'strahlemitter', 'pfeilführung'})
    if muzzle:
        i = max(muzzle, key=lambda j: _box(model[j])[1][0])
        lo, hi = _box(model[i]); point = (lo + hi) / 2; point[0] = hi[0]
        set_anchor('Socket_Muzzle', i, point, 'inferred: named forward functional part front plane and cross-section centre')
    else:
        set_anchor('Socket_Muzzle', source='unavailable', reason='No named muzzle, emitter, barrel or arrow tip.')
    optics = [i for i, p in enumerate(model) if p.sight]
    rail = _anchor_candidates(model, {'visierschiene'})
    if optics:
        lo, hi = bounds([model[i] for i in optics]); point = (lo + hi) / 2; point[1] = hi[1]
        set_anchor('Socket_Sight', point=point, source='inferred: mounted sight assembly bottom centre')
        result['Socket_Sight']['parts'] = [f'p{i:03d}' for i in optics]
    elif rail:
        i = rail[0]; lo, hi = _box(model[i]); point = (lo + hi) / 2; point[1] = lo[1]
        set_anchor('Socket_Sight', i, point, 'inferred: sight rail top centre')
    else:
        set_anchor('Socket_Sight', source='unavailable', reason='No sight assembly or named sight rail.')
    weighted = [(i, float(np.prod(_box(p)[1] - _box(p)[0]))) for i, p in enumerate(model)
                if not getattr(p, 'is_decal', False) and not getattr(p, 'skin_trim', False)]
    volume = sum(weight for _, weight in weighted)
    if volume:
        point = sum(_center(model[i]) * weight for i, weight in weighted) / volume
        set_anchor('Socket_CenterOfMass', point=point, source='approximation: solid part bounding-box volume weighted; sight included; uniform density, not physical mass')
    else:
        set_anchor('Socket_CenterOfMass', source='unavailable', reason='No nonzero solid bounding-box volume.')
    # Explicit points are in native model coordinates. Resolve their part if supplied.
    for key, declaration in meta.get('anchors', {}).items():
        if key not in result:
            raise ValueError(f'Unknown anchor: {key}')
        point = declaration.get('model')
        if point is not None and (np.asarray(point).shape != (3,) or not np.isfinite(point).all()):
            raise ValueError(f'{key}: expected a finite model-space point')
        part = declaration.get('part')
        if part and not (part.startswith('p') and part[1:].isdigit()):
            hits = [i for i, p in enumerate(model) if p.label == part]
            if len(hits) != 1:
                raise ValueError(f'{key}: explicit part label must identify one part')
            part = f'p{hits[0]:03d}'
        if part and part not in {f'p{i:03d}' for i in range(len(model))}:
            raise ValueError(f'{key}: unknown part {part}')
        result[key] = dict(model=None if point is None else _vec(point), part=part,
                           source='explicit: meta.anchors; ' + declaration.get('source', 'model author'),
                           null_reason=declaration.get('null_reason') if point is None else None)
        if point is None and not result[key]['null_reason']:
            raise ValueError(f'{key}: null explicit anchor needs null_reason')
    return result


def _dimensions(parts, convert):
    if not parts:
        return None
    lo, hi = bounds(parts)
    corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    points = convert(corners); low = points.min(axis=0); high = points.max(axis=0)
    return dict(length=float(high[1] - low[1]), height=float(high[2] - low[2]),
                width=float(high[0] - low[0]), bounds_m=[_vec(low), _vec(high)])


def _sight(meta, model, convert, anchors):
    indices = [i for i, p in enumerate(model) if p.sight]
    labels = list(dict.fromkeys(model[i].label for i in indices if model[i].label))
    kind_type = meta.get('sight_type')
    type_source = 'explicit: meta.sight_type'
    if kind_type is None:
        text = ' '.join(labels).casefold()
        kind_type = ('sniper' if meta['slug'] == 'sniper' else 'precision') if ('fernrohr' in text or 'objektiv' in text) else 'reflex' if 'reflex' in text else 'pin' if 'pin' in text else None
        type_source = 'inferred from named sight parts' if kind_type else 'unavailable: no explicit type or recognised sight label'
    if kind_type is not None and kind_type not in SIGHT_TYPES:
        raise ValueError(f'Unknown sight_type: {kind_type}')
    kind, window = SIGHT_TYPES.get(kind_type, (None, None))
    frame = meta.get('sight_frame')
    frame_source = 'explicit: meta.sight_frame'
    if frame is None:
        text = ' '.join(labels).casefold()
        frame = 'open' if 'rahmen' in text or 'brücke' in text else 'standard' if 'fernrohr' in text else None
        frame_source = 'inferred from named frame construction' if frame else 'unavailable: frame construction not declared'
    elements = []
    for i in indices:
        p = model[i]
        explicit = getattr(p, 'sight_window', False)
        aperture = getattr(p, 'window_geometry', None)
        if aperture is not None:
            centre = np.asarray(aperture['center_model'], dtype=float)
            normal = np.asarray(aperture['normal_model'], dtype=float)
            if centre.shape != (3,) or normal.shape != (3,) or not np.isfinite(centre).all() or not np.isfinite(normal).all() or np.linalg.norm(normal) < 1e-9:
                raise ValueError('Functional sight aperture needs finite centre and nonzero normal')
            normal = normal / np.linalg.norm(normal)
            view = M @ normal
            if view[1] > 0:
                view = -view
            elements.append(dict(part=f'p{i:03d}', label=p.label, type='open_aperture',
                                 source=aperture.get('source', 'explicit: part.window_geometry'),
                                 center_model=_vec(centre), center_m=_vec(convert(centre)),
                                 normal_model=_vec(normal), view_axis_m=_vec(view),
                                 width_m=float(aperture['width_model']) * float(np.linalg.norm(convert(centre + [0, 0, 1]) - convert(centre))),
                                 height_m=float(aperture['height_model']) * float(np.linalg.norm(convert(centre + [0, 1, 0]) - convert(centre))),
                                 forward_aligned=bool(abs(view[1]) > .99),
                                 null_reason=None,
                                 note='Explicit clear aperture, not a filled glass slab; frame solid faces do not define its view axis.'))
            if elements[-1]['width_m'] <= 0 or elements[-1]['height_m'] <= 0:
                raise ValueError('Functional sight aperture dimensions must be positive')
            continue
        if not explicit and (p.label or '').casefold() not in {'sichtfenster', 'visierglas', 'optikglas', 'linse', 'fensterscheibe'}:
            continue
        lo, hi = _box(p); extent = hi - lo
        axis = int(np.argmin(extent))
        sorted_extent = np.sort(extent)
        unique = bool(sorted_extent[1] > 0 and sorted_extent[0] < sorted_extent[1] * .4)
        view = M[:, axis] if unique else None
        if view is not None and view[1] > 0:
            view = -view
        elements.append(dict(part=f'p{i:03d}', label=p.label,
                             source='explicit: part.sight_window' if explicit else 'inferred: named optical surface',
                             bounds_m=_dimensions([p], convert)['bounds_m'],
                             model_thin_axis='XYZ'[axis] if unique else None,
                             view_axis_m=None if view is None else _vec(view),
                             forward_aligned=None if view is None else bool(abs(view[1]) > .99),
                             null_reason=None if unique else 'No unique thin optical axis; geometry needs inspection.'))
    return dict(present=bool(indices), type=kind_type, type_source=type_source,
                kind=kind, window=window, window_geometry_kind='open' if any(e.get('type') == 'open_aperture' for e in elements) else 'surface' if elements else None,
                window_source='Requested sight-type vocabulary; physical construction described separately by window_geometry',
                frame=frame, frame_source=frame_source,
                modular=True, mount_side='left' if meta['slug'] == 'rocket' else 'top',
                labels=labels, parts=[f'p{i:03d}' for i in indices],
                bounds_m=_dimensions([model[i] for i in indices], convert)['bounds_m'] if indices else None,
                anchor=anchors['Socket_Sight'], window_geometry=elements or None,
                window_geometry_note=None if elements else 'No declared/named optical surface; frame bounding box is not evidence of a functional window.')


def _palettes(meta, model, exported, record):
    variants = record.get('palette_variants') or [dict(name='BASIS', colors=meta['palette'])]
    result = []
    for variant in variants:
        colors = variant['colors']
        if len(colors) != 4:
            raise ValueError('Palette must contain four renderer swatches')
        default = dict(zip(CHANNELS, (colors[0], colors[1], colors[3], colors[1], colors[3], colors[3], colors[2])))
        role_colors = dict(zip(('primary', 'medium', 'dark', 'accent'), colors))
        entries = {}
        for channel in CHANNELS:
            areas = {}
            for p, data in zip(model, exported):
                if data['channel'] == channel:
                    color = p.color if variant['name'] == 'BASIS' else role_colors.get(p.role, p.color)
                    areas[color] = areas.get(color, 0.) + data['area_m2']
            ordered = sorted(areas, key=lambda c: (-areas[c], c))
            entries[channel] = dict(color=ordered[0] if ordered else default[channel],
                                    source='largest surface area in channel' if ordered else 'swatch fallback; channel unused',
                                    other_colors=[dict(color=c, area_m2=areas[c]) for c in ordered[1:]])
        result.append(dict(name=variant['name'], swatches=list(colors), channels=entries,
                           sight_colors='palette remap metadata; mounted optic rendering is documented by sheet'))
    return result


def _robot_fit(meta, model, anchors, scale, dimensions):
    slug = meta['slug']
    def sourced(value):
        return dict(value=value, source=FIT_SOURCE)
    def measured(value, source, limit=None, minimum=False):
        return dict(value=value, source=source, ok=None if value is None or limit is None else bool(value >= limit if minimum else value <= limit),
                    null_reason='Required named geometry/anchor unavailable.' if value is None else None)
    muzzle = anchors['Socket_Muzzle']['part']
    barrel = None
    if muzzle:
        p = model[int(muzzle[1:])]; lo, hi = _box(p)
        barrel = float(min((hi - lo)[1:]) * scale)
    receivers = _anchor_candidates(model, {'gehäuse'})
    receiver = max((float((_box(model[i])[1][1] - _box(model[i])[0][1]) * scale) for i in receivers), default=None)
    support = anchors['Socket_SupportHand']['position_m']
    behind = max(0., float(dimensions['with_sight']['bounds_m'][1][1]))
    target_length = FIT_LENGTHS_M.get(slug)
    target_scale = target_length / dimensions['with_sight']['length'] if target_length else None
    measurements = dict(
        length_m=measured(dimensions['with_sight']['length'], 'Mounted model longitudinal extent'),
        support_forward_m=measured(None if support is None else -support[1], 'Socket_SupportHand relative to Socket_Hand', .10),
        stock_behind_m=measured(behind, 'Rear mounted-model bound behind Socket_Hand; conservative stock envelope', .12),
        barrel_m=measured(barrel, 'Smaller cross-section extent of named muzzle part; outer envelope, not bore diameter', .03, True),
        receiver_height_m=measured(receiver, 'Largest named Gehäuse height', .08, True))
    targets = {key: sourced(value) for key, value in dict(support_hand_max_forward_m=.10,
               stock_max_behind_m=.12, barrel_min_m=.03, receiver_min_height_m=.08, silhouette_factor=1.5).items()} if target_length else {}
    if target_length:
        targets['length_m'] = sourced(target_length)
    elif slug == 'pistol':
        targets['length_min_m'] = sourced(.24)
    at_target = None
    if target_scale:
        at_target = dict(scale=target_scale, source='Uniform hypothetical rescale to robot target length; not applied to exported model', measurements={})
        limits = dict(support_forward_m=(.10, False), stock_behind_m=(.12, False), barrel_m=(.03, True), receiver_height_m=(.08, True))
        for key, item in measurements.items():
            value = None if item['value'] is None else item['value'] * target_scale
            limit, minimum = limits.get(key, (None, False))
            at_target['measurements'][key] = measured(value, item['source'] + '; uniformly rescaled', limit, minimum)
    return dict(source=FIT_SOURCE, concept_sheets=False, applies=target_length is not None,
                reason=None if target_length else 'Pistol uses cup grip; no long-gun fit target.' if slug == 'pistol' else 'No robot bow-fit target defined.',
                robot={key: sourced(value) for key, value in dict(height_m=1.50, hand_m=.09, arm_m=.42).items()},
                targets=targets, actual=measurements, sheet_at_target=at_target,
                validated=False, fits_robot=None,
                validation_note='Envelope measurements only; robot hand mesh, articulation, collision and grip pose have not been tested. Silhouette factor is a target, not measured compliance.')


def design_spec(meta, model, number, record):
    """Serialize base model, declared decisions and explicitly marked inferences."""
    from skins import CATALOG
    if not model or not any(not p.sight for p in model):
        raise ValueError('Reference requires a nonempty weapon model')
    slug = meta['slug']
    if slug not in LENGTHS_M:
        raise ValueError(f'No documented reference scale for {slug}')
    lo, hi = bounds([p for p in model if not p.sight])
    all_lo, all_hi = bounds(model)
    extent = all_hi - all_lo
    length_units = float(np.max(extent) if slug == 'bow' else extent[0])
    if length_units <= 0:
        raise ValueError('Reference length must be positive')
    scale = LENGTHS_M[slug] / length_units
    anchors = _anchors(meta, model)
    hand = anchors['Socket_Hand']['model']
    if hand is None:
        raise ValueError('Socket_Hand unavailable: cannot claim a hand-relative metre frame')
    origin = np.asarray(hand)
    def convert(points):
        return (np.asarray(points) - origin) @ M.T * scale
    for anchor in anchors.values():
        anchor['position_m'] = None if anchor['model'] is None else _vec(convert(anchor['model']))
    exported = []
    for i, p in enumerate(model):
        channel, channel_source = _channel(p)
        data = dict(id=f'p{i:03d}', label=p.label, role=p.role, color=p.color,
                    material=p.material, emit=p.emit, sight=p.sight,
                    faces=[dict(vertices=np.asarray(f.vertices).round(7).tolist(), normal=np.asarray(f.normal).round(7).tolist()) for f in p.faces],
                    channel=channel, channel_source=channel_source,
                    area_m2=_surface_area(p) * scale ** 2,
                    bounds_m=_dimensions([p], convert)['bounds_m'],
                    finish=getattr(p, 'finish', None), skin_trim=bool(getattr(p, 'skin_trim', False)))
        exported.append(data)
    dimensions = dict(weapon=_dimensions([p for p in model if not p.sight], convert),
                      with_sight=_dimensions(model, convert))
    skins = deepcopy(CATALOG)
    for skin in skins:
        ingredients, finishes = SKIN_DETAILS.get(skin['id'], ([], []))
        skin['ingredients'] = list(ingredients)
        skin['finishes'] = list(finishes)
        skin['recipe_source'] = 'skins.sample_surface/apply_skin and raster._finish_surface'
    hero = record.get('main_skin', skins[0]['id'])
    if isinstance(hero, dict):
        hero = hero['id']
    if len(skins) != 5:
        raise ValueError('Design reference requires exactly five skin catalog entries')
    moving = deepcopy(meta.get('moving_parts'))
    if moving is None:
        moving = dict(root_moves=False, frame='metre reference frame', items=None,
                      source='No motion rig or authored motion declarations in this static concept model.',
                      null_reason='Moving assemblies, pivots and travel have not been declared; labels alone do not establish animation.')
    return dict(format='CodexDesignReference', version=1, reference_revision=2,
        sheet=dict(id=f"K{meta['variant']}{number:02d}", variant=meta['variant'],
                   variant_name=meta['variant_name'], name=meta['name'], kind=meta['kind'], number=number, series=meta.get('series')),
        reference_only=True,
        compatibility=dict(toolgen_import_validated=False, schema='Independent CodexDesignReference; not cubeescape-design/weapon-spec',
                           note='Shared axis/target vocabulary only. A consumer adapter and schema/mesh validation are still required.'),
        axes=dict(forward='+X', down='+Y', left='+Z', units='model units (raw faces and bounding_box)',
                  target=dict(forward='-Y', up='+Z', left='+X', units='m', origin='Socket_Hand'),
                  matrix_model_to_m=M.tolist(), formula='p_m = model_unit_m * M @ (p_model - Socket_Hand.model)',
                  handedness='right', origin_model=_vec(origin)),
        units=dict(model_unit_m=scale, model_length_units=length_units, reference_length_m=LENGTHS_M[slug],
                   rule='Largest mounted extent for bow; mounted longitudinal X extent for other classes.', source=REFERENCE_SOURCE),
        bounding_box=[lo.tolist(), hi.tolist()], dimensions_m=dimensions, anchors=anchors,
        construction_notes=meta['notes'], form=meta['form'], palette=meta['palette'],
        palette_variants=_palettes(meta, model, exported, record),
        channels_used=sorted({p['channel'] for p in exported}),
        skin=dict(hero=hero, catalog=skins, items=deepcopy(record.get('skins', skins)),
                  channel_slots=list(CHANNELS), fixed_slots=['SK_Accent1', 'SK_Accent2'],
                  space='native model object coordinates; convert with units/axes to hand-relative metres',
                  source='Independent skins.CATALOG and apply_skin/raster implementation; base parts exported here',
                  geometry_note='Catalog trim is generated by apply_skin; raw parts above describe the unskinned reference.'),
        textures=dict(frame='native model object coordinates', source='raster._texture; renderer preview shading, not baked PBR or UV maps',
                      paint='subtle broad surface variation', metal='directional brushing', rubber='crossed knurl grooves',
                      plastic='fine grain', light='uniform emissive', physical_recipe_validated=False),
        moving_parts=moving, sight=_sight(meta, model, convert, anchors),
        robot_fit=_robot_fit(meta, model, anchors, scale, dimensions),
        orthographic_views=record['orthographic_views'], geometry_sha256=record['geometry_sha256'], parts=exported)
