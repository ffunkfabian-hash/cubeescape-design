"""Conservative label matching for the documented Weapon-Spec v1 use-clip table.

Axes come from the shared contract; missing named components remain null. This
is not an animation rig or a claim that the static design has tested travel.
"""
SOURCE='claude/docs/weapon-spec.md#bewegliche-teile (use-clip contract; static Codex labels)'
PLANS={
 'pistol': [('slide','Schlitten','Anim_Slide',[('translate',[0,1,0])],('schlitten','verschluss'))],
 'assault': [('bolt','Verschluss','Anim_Bolt',[('translate',[0,1,0])],('verschluss','ladehebel','spannhebel'))],
 'smg': [('bolt','Verschluss','Anim_Bolt',[('translate',[0,1,0])],('verschluss','ladehebel','spannhebel'))],
 'trace': [('bolt','Verschluss','Anim_Bolt',[('translate',[0,1,0])],('verschluss','ladehebel','spannhebel'))],
 'impulse': [('cell','Pulszelle','Anim_Cell',[('translate',[0,1,0])],('pulszelle','pulswürfel','kristallkern','energiekugel'))],
 'shotgun': [('pump','Pumpgriff','Anim_Bolt',[('translate',[0,1,0])],('pumpgriff','repetierschieber','pumpmanschette'))],
 'sniper': [('lever','Kammerstängel','Anim_Bolt',[('rotate',[0,1,0]),('translate',[0,1,0])],('kammerstängel','kammerhebel','kammer','verschluss'))],
 'fusion': [('fins','Flossen','Anim_FinL/R',[('rotate',[0,0,1])],('flosse','flossen','finne','finnen')),
            ('coil','Spulenring','Anim_Coil',[('rotate',[0,1,0])],('spulenring','beschleunigerring'))],
 'rocket': [('hatch','Ladeklappe','Anim_Hatch',[('rotate',[1,0,0])],('ladeklappe','klappe'))],
 'bow': []}


def make_moving_parts(meta,model):
    if meta['slug'] in PROPOSED:
        return _make_proposed_parts(meta,model)
    items=[]
    for kind,name,node,motions,labels in PLANS[meta['slug']]:
        found=[(i,p) for i,p in enumerate(model) if not p.sight and p.label.casefold() in labels]
        matched=[f'p{i:03d}' for i,_ in found]
        actual=[p.label for _,p in found]
        source=SOURCE
        if not found:source+='; no named compatible component; magazine energy cells and cooling ribs are not use-clip parts.'
        else:source+='; exact static component label; motion axis is the documented target, not a measured animation.'
        items.append({'kind':kind,'name_de':name,'toolgen_node':node,
                      'motions':[{'type':typ,'axis':axis} for typ,axis in motions],
                      'parts':matched or None,'labels':actual,'match':'similar' if found and 'Pumpmanschette' in actual else 'label' if found else None,
                      'source':source})
    return {'source':SOURCE,'root_moves':False,'frame':'Toolgen/Blender metre frame: forward -Y, up +Z; local motion axes.',
            'items':items,'note':'No bow use-clip entry is defined; arrow is a separate static projectile assembly.' if meta['slug']=='bow' else
                    'Contract motion targets with conservative label mapping; pivots, travel, timing and actual rig are unvalidated.'}

# New motion axes and node names are explicit proposals. Nothing here asserts
# a tested Toolgen clip or a physically verified pivot/travel.
PROPOSED = {
 'scout':[('bolt','Verschluss','Anim_Bolt','translate',[0,1,0],('Verschluss',))],
 'handcannon':[('cylinder','Trommel','Anim_Cylinder','rotate',[0,1,0],('Trommel',)),('hammer','Hahn','Anim_Hammer','rotate',[1,0,0],('Hahn',))],
 'linear':[('rails','Beschleunigerschienen','Anim_Rails','translate',[1,0,0],('Beschleunigerschiene',))],
 'breech':[('breech','Kipplauf','Anim_Breech','rotate',[1,0,0],('Kipplauf','Lauf','Mündung'))],
 'drum':[('drum','Granattrommel','Anim_Drum','rotate',[0,1,0],('Granattrommel',)),('hatch','Ladeklappe','Anim_Hatch','rotate',[0,0,1],('Ladeklappe',))],
 'machine':[('bolt','Verschluss','Anim_Bolt','translate',[0,1,0],('Verschluss',)),('feed_cover','Zuführdeckel','Anim_FeedCover','rotate',[1,0,0],('Zuführdeckel',))],
 'sword':[],
 'glaive':[('shield','Schildflügel','Anim_Shield','rotate',[0,1,0],('Schildflügel',))],
 'crossbow':[('cocking','Spannhebel','Anim_Cocking','rotate',[1,0,0],('Spannhebel',)),('string','Sehne','Anim_String','translate',[0,1,0],('Sehne',))],
 'rocketside':[('slide','Schlitten','Anim_Slide','translate',[0,1,0],('Schlitten',))],
 'rocketpulse':[('bolt','Verschluss','Anim_Bolt','translate',[0,1,0],('Verschluss',))],
 'slug':[('bolt','Verschluss','Anim_Bolt','translate',[0,1,0],('Verschluss',))],
 'heat':[('vent','Entlüftungsklappen','Anim_Vent','rotate',[0,1,0],('Entlüftungsklappe',))],
 'micro':[('hatch','Ladeklappe','Anim_Hatch','rotate',[1,0,0],('Ladeklappe',))],
 'spread':[('top_break','Kipprahmen','Anim_TopBreak','rotate',[1,0,0],('Kipprahmen','Lauf','Mündung','Trommel'))],
}

def _make_proposed_parts(meta, model):
    source = 'Codex-Konstruktionsvorschlag; Knotennamen und Bewegungsachsen abgeleitet, nicht in Toolgen/Spiel angebunden.'
    items = []
    for kind, german, node, motion, axis, labels in PROPOSED[meta['slug']]:
        matches = [(i,p) for i,p in enumerate(model) if not p.sight and p.label in labels]
        items.append(dict(kind=kind,name_de=german,toolgen_node=node,
                          motions=[dict(type=motion,axis=axis)],
                          parts=[f'p{i:03d}' for i,_ in matches] or None,
                          labels=list(dict.fromkeys(p.label for _,p in matches)),
                          match='label' if matches else None,proposed=True,
                          source=source + ('' if matches else ' Kein entsprechendes benanntes Außenteil vorhanden.')))
    return dict(source=source,root_moves=False,proposed=True,
                frame='Toolgen/Blender metre frame: forward -Y, up +Z; local motion axes.',items=items,
                note='Vorschlag: Pivot, Hub, Timing, Abhängigkeiten und Spielfunktion sind nicht geprüft.')
