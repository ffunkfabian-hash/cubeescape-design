#!/usr/bin/env python3
"""Erzeugt claude/output/index.html: statische Galerie aller Konzeptblätter.

Liest nur vorhandene Dateien (nichts fest verdrahtet, neue Varianten erscheinen von selbst):
  claude/output/sheets/K??NN.spec.json   Metadaten (sheet.variant, sheet.number, sheet.nick,
                                         optional sheet.variant_name, weapon.name_de, skin.hero)
  claude/output/sheets/K??NN.dc.html     Blatt XL (öffnet direkt im Browser, support.js fehlt folgenlos)
  claude/output/previews/K??NN.webp      Vorschau 1600 px
  claude/output/sheets/VSNN.spec.json    Visier-Serie (Sight-Spec, claude-0.6), Gruppe „VS“
  codex/**/output/*.html                 nur falls vorhanden, nur verlinkt (Codex-Ordner wird nie geschrieben)

Die Seite ist offline per Doppelklick (file://) nutzbar, alle Links relativ.
Aufruf: python3 claude/generator/make_viewer.py [--out PFAD]
"""
import argparse
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT_DIR = REPO / "claude" / "output"
SHEETS = OUT_DIR / "sheets"
PREVIEWS = OUT_DIR / "previews"
SHEET_RE = re.compile(r"^K([A-Z])(\d{2})$")


def _title_of(path):
    m = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8", errors="replace")[:4000], re.S)
    return html.unescape(m.group(1).strip()) if m else ""


def collect_sheets():
    items = {}
    for spec in sorted(SHEETS.glob("K*.spec.json")):
        try:
            d = json.loads(spec.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"WARNUNG: {spec.name} nicht lesbar ({e}), übersprungen")
            continue
        s = d.get("sheet") or {}
        w = d.get("weapon") or {}
        sid = s.get("id") or spec.name.split(".")[0]
        skin = d.get("skin") if isinstance(d.get("skin"), dict) else {}
        items[sid] = {
            "id": sid,
            "variant": s.get("variant") or sid[1:2],
            "variant_name": s.get("variant_name") or "",
            "number": str(s.get("number") or sid[2:4]),
            "nick": s.get("nick") or "",
            "weapon": w.get("name_de") or "",
            "weapon_id": w.get("toolgen_id") or "",
            "skin": skin.get("hero") or "",
            "element": d.get("element") if isinstance(d.get("element"), str) else "",
            "sheet": s.get("file") or f"{sid}.dc.html",
            "spec": spec.name,
        }
    # Visier-Serie (claude-0.6): VSnn.spec.json (Sight-Spec), im Viewer als eigene Gruppe „VS · Visier-Serie“
    for spec in sorted(SHEETS.glob("VS*.spec.json")):
        try:
            d = json.loads(spec.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"WARNUNG: {spec.name} nicht lesbar ({e}), übersprungen")
            continue
        s, w, sg = d.get("sheet") or {}, d.get("weapon") or {}, d.get("sight") or {}
        sid = s.get("id") or spec.name.split(".")[0]
        items[sid] = {"id": sid, "variant": "VS", "variant_name": s.get("series_name_de") or "Visier-Serie",
                      "number": str(s.get("number") or sid[2:4]), "nick": sg.get("title_de") or "",
                      "weapon": w.get("name_de") or "", "weapon_id": w.get("toolgen_id") or "", "skin": "",
                      "element": sg.get("type") or "", "sheet": s.get("file") or f"{sid}.dc.html", "spec": spec.name}
    # Blätter ohne Spec (z. B. halb gebaute Variante) trotzdem zeigen, Daten aus Dateiname und <title>.
    for f in sorted(SHEETS.glob("K*.dc.html")):
        sid = f.name[: -len(".dc.html")]
        m = SHEET_RE.match(sid)
        if not m or sid in items:
            continue
        items[sid] = {"id": sid, "variant": m.group(1), "variant_name": "", "number": m.group(2),
                      "nick": "", "weapon": "", "weapon_id": "", "skin": "", "element": "",
                      "sheet": f.name, "spec": "", "title": _title_of(f)}
    for it in items.values():
        it["sheet"] = "sheets/" + it["sheet"] if (SHEETS / it["sheet"]).exists() else ""
        it["spec"] = "sheets/" + it["spec"] if it["spec"] else ""
        prev = PREVIEWS / f"{it['id']}.webp"
        it["preview"] = "previews/" + prev.name if prev.exists() else ""
    # Variantenname, falls nur ein Teil der Blätter ihn trägt, auf die ganze Variante übertragen.
    names = {}
    for it in items.values():
        if it["variant_name"]:
            names.setdefault(it["variant"], it["variant_name"])
    for it in items.values():
        it["variant_name"] = it["variant_name"] or names.get(it["variant"], "")
    # Waffentyp für Blätter ohne Spec über die Nummer aus anderen Varianten ableiten.
    by_num = {it["number"]: it["weapon"] for it in items.values() if it["weapon"]}
    for it in items.values():
        it["weapon"] = it["weapon"] or by_num.get(it["number"], "")
    return sorted(items.values(), key=lambda it: (it["variant"], it["number"]))


def collect_codex():
    """Codex-Blätter nur lesen und verlinken, falls codex/ in dieser Arbeitskopie existiert."""
    root = REPO / "codex"
    out = []
    if not root.is_dir():
        return out
    for f in sorted(root.glob("**/output/*.html")):
        rel = Path("..", "..", f.relative_to(REPO)).as_posix()
        out.append({"name": f.stem, "path": rel, "group": f.parent.parent.name, "title": _title_of(f)})
    return out


PAGE = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Konzeptblätter · Cube Escape Design</title>
<style>
:root{--bg:#0E1622;--panel:#152131;--line:#26364a;--fg:#E6ECF2;--mute:#8FA0B3;--acc:#FFD166;--acc2:#4CC9F0}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 Barlow,system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--acc2)}
header{position:sticky;top:0;z-index:5;background:rgba(14,22,34,.96);border-bottom:1px solid var(--line);padding:12px 20px;display:flex;flex-direction:column;gap:10px;backdrop-filter:blur(6px)}
.top{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
h1{font:700 20px/1 "Chakra Petch",system-ui,sans-serif;letter-spacing:2px;margin:0;color:var(--acc)}
#count{color:var(--mute)}
#q{flex:1 1 220px;max-width:360px;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:7px 10px;font:inherit}
.row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.lab{color:var(--mute);font-size:12px;letter-spacing:1px;text-transform:uppercase;width:72px}
.chip{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:999px;padding:4px 11px;font:inherit;font-size:13px;cursor:pointer}
.chip:hover{border-color:var(--mute)}
.chip.on{background:var(--acc);border-color:var(--acc);color:#111}
.chip small{opacity:.7}
main{padding:16px 20px 40px}
.group h2{font:600 15px/1.2 "Chakra Petch",system-ui,sans-serif;letter-spacing:1.5px;color:var(--mute);margin:18px 0 10px;text-transform:uppercase}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;transition:border-color .1s}
.card:hover,.card:focus{border-color:var(--acc);outline:none}
.thumb{aspect-ratio:4800/4432;background:#0a111a;display:flex;align-items:center;justify-content:center;color:var(--mute)}
.thumb img{width:100%;height:100%;object-fit:contain;display:block}
.meta{padding:8px 10px;display:flex;flex-direction:column;gap:2px}
.meta b{font-family:"Chakra Petch",system-ui,sans-serif;letter-spacing:1px}
.meta span{color:var(--mute);font-size:12.5px}
.empty{color:var(--mute);padding:40px 0;text-align:center}
#codex ul{margin:0;padding-left:18px;columns:3 240px}
#lb{position:fixed;inset:0;z-index:10;background:rgba(5,9,14,.97);display:flex;flex-direction:column}
#lb[hidden]{display:none}
.lbbar{display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.lbbar .t{font:600 16px/1.2 "Chakra Petch",system-ui,sans-serif;letter-spacing:1px;flex:1 1 auto;min-width:200px}
.lbbar .t small{color:var(--mute);font-family:Barlow,system-ui,sans-serif;letter-spacing:0;font-weight:400}
.btn{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:5px 10px;font:inherit;font-size:13px;cursor:pointer;text-decoration:none;white-space:nowrap}
.btn:hover{border-color:var(--mute)}
.btn.on{border-color:var(--acc);color:var(--acc)}
#stage{flex:1;position:relative;overflow:auto;display:flex}
#stage img{margin:auto;max-width:100%;max-height:100%;object-fit:contain;cursor:zoom-in}
#stage.zoom img{max-width:none;max-height:none;cursor:zoom-out}
#frameBox{margin:auto;position:relative;flex:none}
#frameBox iframe{border:0;transform-origin:0 0;position:absolute;left:0;top:0;background:var(--bg)}
.nav{position:fixed;top:50%;transform:translateY(-50%);z-index:11;background:rgba(21,33,49,.8);color:var(--fg);border:1px solid var(--line);width:44px;height:64px;border-radius:8px;font-size:26px;cursor:pointer}
.nav:hover{border-color:var(--acc)}
#prev{left:10px}#next{right:10px}
.hint{color:var(--mute);font-size:12px}
@media (max-width:600px){.lab{width:auto}.nav{width:34px;height:50px}}
</style>
</head>
<body>
<header>
  <div class="top">
    <h1>KONZEPTBLÄTTER</h1>
    <input id="q" type="search" placeholder="Suche: Spitzname, Waffe, Nummer, Skin …" autocomplete="off">
    <span id="count"></span>
    <span class="row" style="margin-left:auto"><span class="hint">Gruppieren:</span>
      <button class="chip" data-group="variant">Variante</button><button class="chip" data-group="weapon">Waffe</button></span>
  </div>
  <div class="row" id="fVar"><span class="lab">Variante</span></div>
  <div class="row" id="fWeap"><span class="lab">Waffe</span></div>
</header>
<main>
  <div id="list"></div>
  <section id="codex" hidden><div class="group"><h2>Codex (nur Links, Ordner codex/)</h2><ul></ul></div></section>
</main>
<div id="lb" hidden>
  <div class="lbbar">
    <div class="t" id="lbT"></div>
    <button class="btn" id="mPrev" title="Vorschau-Bild (V)">Vorschau</button>
    <button class="btn" id="mXL" title="Blatt XL im Viewer (X)">Blatt XL</button>
    <button class="btn" id="zoomB" title="Zoom (Z)">Zoom: eingepasst</button>
    <a class="btn" id="aSheet" target="_blank">Blatt in neuem Tab</a>
    <a class="btn" id="aSpec" target="_blank">spec.json</a>
    <a class="btn" id="aImg" target="_blank">WebP</a>
    <span class="hint" id="pos"></span>
    <button class="btn" id="close" title="Schließen (Esc)">✕</button>
  </div>
  <div id="stage"></div>
  <button class="nav" id="prev" title="Zurück (←)">‹</button>
  <button class="nav" id="next" title="Weiter (→)">›</button>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
const D = JSON.parse(document.getElementById('data').textContent);
const S = D.sheets, $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let st = {v:new Set(), w:new Set(), q:'', group:'variant'};
try { const g = localStorage.getItem('cev.group'); if (g) st.group = g; } catch(e) {}
let shown = [], cur = -1, mode = 'img', zoom = false;

// Filterlisten nur aus den Daten: Varianten nach Buchstabe, Waffen nach Nummer.
const variants = [...new Map(S.map(s => [s.variant, s.variant_name])).entries()].sort();
const weapons = [...new Map(S.slice().sort((a,b)=>a.number.localeCompare(b.number)).map(s => [s.weapon || ('Nr. ' + s.number), s.number])).entries()];
const vLabel = (v, n) => n ? `${v} <small>${esc(n)}</small>` : v;
const wName = s => s.weapon || ('Nr. ' + s.number);
function chips(box, entries, set, label){
  for (const [key, extra] of entries){
    const b = document.createElement('button'); b.className = 'chip'; b.innerHTML = label(key, extra); b.dataset.k = key;
    b.onclick = () => { set.has(key) ? set.delete(key) : set.add(key); b.classList.toggle('on'); render(); };
    box.appendChild(b);
  }
  const a = document.createElement('button'); a.className = 'chip'; a.textContent = 'alle';
  a.onclick = () => { set.clear(); box.querySelectorAll('.chip.on').forEach(x => x.classList.remove('on')); render(); };
  box.appendChild(a);
}
chips($('#fVar'), variants, st.v, vLabel);
chips($('#fWeap'), weapons, st.w, (k, n) => `${n} ${esc(k)}`);
document.querySelectorAll('[data-group]').forEach(b => b.onclick = () => {
  st.group = b.dataset.group; try { localStorage.setItem('cev.group', st.group); } catch(e) {} render(); });
$('#q').oninput = e => { st.q = e.target.value.trim().toLowerCase(); render(); };

const hay = s => [s.id, s.nick, s.weapon, s.weapon_id, s.number, s.variant, s.variant_name, s.skin, s.element, s.title||''].join(' ').toLowerCase();
function title(s){ return `${s.number} ${esc(wName(s))} · Variante ${s.variant}${s.variant_name ? ' ' + esc(s.variant_name) : ''}`; }
function render(){
  document.querySelectorAll('[data-group]').forEach(b => b.classList.toggle('on', b.dataset.group === st.group));
  const words = st.q.split(/\s+/).filter(Boolean);
  shown = S.filter(s => (!st.v.size || st.v.has(s.variant)) && (!st.w.size || st.w.has(wName(s)))
                      && words.every(w => hay(s).includes(w)));
  if (st.group === 'weapon') shown.sort((a,b) => a.number.localeCompare(b.number) || a.variant.localeCompare(b.variant));
  $('#count').textContent = `${shown.length} von ${S.length} Blättern`;
  const groups = new Map();
  shown.forEach((s, i) => {
    const k = st.group === 'weapon' ? `${s.number} ${wName(s)}` : `Variante ${s.variant}${s.variant_name ? ' · ' + s.variant_name : ''}`;
    if (!groups.has(k)) groups.set(k, []); groups.get(k).push([s, i]);
  });
  let h = '';
  for (const [k, arr] of groups){
    h += `<div class="group"><h2>${esc(k)}</h2><div class="grid">`;
    for (const [s, i] of arr){
      const img = s.preview ? `<img loading="lazy" src="${esc(s.preview)}" alt="${esc(s.id)}">` : 'keine Vorschau';
      h += `<div class="card" tabindex="0" data-i="${i}"><div class="thumb">${img}</div><div class="meta">
        <b>${esc(s.id)} · ${esc(s.nick || s.title || '–')}</b><span>${title(s)}${s.skin ? ' · Skin ' + esc(s.skin) : ''}</span></div></div>`;
    }
    h += '</div></div>';
  }
  $('#list').innerHTML = h || '<div class="empty">Keine Treffer.</div>';
}
$('#list').addEventListener('click', e => { const c = e.target.closest('.card'); if (c) open(+c.dataset.i); });
$('#list').addEventListener('keydown', e => { const c = e.target.closest('.card'); if (c && e.key === 'Enter') open(+c.dataset.i); });

function setLink(a, href){ a.hidden = !href; if (href) a.href = href; }
function open(i){
  if (!shown.length) return;
  cur = (i + shown.length) % shown.length; const s = shown[cur];
  $('#lbT').innerHTML = `${esc(s.id)} · „${esc(s.nick || s.title || '–')}“ <small>${title(s)}${s.skin ? ' · Skin ' + esc(s.skin) : ''}</small>`;
  $('#pos').textContent = `${cur + 1} / ${shown.length}`;
  setLink($('#aSheet'), s.sheet); setLink($('#aSpec'), s.spec); setLink($('#aImg'), s.preview);
  if (mode === 'img' && !s.preview) mode = 'xl';
  if (mode === 'xl' && !s.sheet) mode = 'img';
  $('#mPrev').classList.toggle('on', mode === 'img'); $('#mXL').classList.toggle('on', mode === 'xl');
  $('#mPrev').disabled = !s.preview; $('#mXL').disabled = !s.sheet;
  const stage = $('#stage'); stage.classList.toggle('zoom', zoom); stage.scrollTo(0, 0);
  $('#zoomB').textContent = zoom ? 'Zoom: 100 %' : 'Zoom: eingepasst';
  if (mode === 'img') {
    stage.innerHTML = `<img src="${esc(s.preview)}" alt="${esc(s.id)}">`;
    stage.firstChild.onclick = () => { zoom = !zoom; open(cur); };
  } else {
    stage.innerHTML = `<div id="frameBox"><iframe src="${esc(s.sheet)}" title="${esc(s.id)}" scrolling="no"></iframe></div>`;
    fitFrame();
  }
  $('#lb').hidden = false; document.body.style.overflow = 'hidden';
  try { history.replaceState(null, '', '#' + s.id); } catch(e) {}
}
// Blatt XL: Originalgröße aus dem Blatt (4800 × 4432), auf die Bühne eingepasst oder 1:1 zum Scrollen.
function fitFrame(){
  const box = document.getElementById('frameBox'); if (!box) return;
  const W = 4800, H = 4432, stage = $('#stage');
  const k = zoom ? 1 : Math.min(stage.clientWidth / W, stage.clientHeight / H);
  const f = box.firstChild; f.style.width = W + 'px'; f.style.height = H + 'px'; f.style.transform = `scale(${k})`;
  box.style.width = W * k + 'px'; box.style.height = H * k + 'px';
}
function close(){ $('#lb').hidden = true; $('#stage').innerHTML = ''; document.body.style.overflow = '';
  try { history.replaceState(null, '', location.pathname + location.search); } catch(e) {} }
$('#prev').onclick = () => open(cur - 1); $('#next').onclick = () => open(cur + 1);
$('#close').onclick = close;
$('#mPrev').onclick = () => { mode = 'img'; open(cur); }; $('#mXL').onclick = () => { mode = 'xl'; open(cur); };
$('#zoomB').onclick = () => { zoom = !zoom; open(cur); };
addEventListener('resize', fitFrame);
addEventListener('keydown', e => {
  if ($('#lb').hidden) { if (e.key === '/' && document.activeElement !== $('#q')) { e.preventDefault(); $('#q').focus(); } return; }
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); open(cur + 1); }
  else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); open(cur - 1); }
  else if (e.key === 'Escape') close();
  else if (e.key === 'x' || e.key === 'X') { mode = 'xl'; open(cur); }
  else if (e.key === 'v' || e.key === 'V') { mode = 'img'; open(cur); }
  else if (e.key === 'z' || e.key === 'Z') { zoom = !zoom; open(cur); }
});

const cx = D.codex;
if (cx.length) {
  $('#codex').hidden = false;
  $('#codex ul').innerHTML = cx.map(c => `<li><a href="${esc(c.path)}" target="_blank">${esc(c.group)}/${esc(c.name)}</a> <span class="hint">${esc(c.title)}</span></li>`).join('');
}
render();
const h = decodeURIComponent(location.hash.slice(1)), hi = shown.findIndex(s => s.id === h);
if (hi >= 0) open(hi);
})();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(OUT_DIR / "index.html"))
    a = ap.parse_args()
    sheets = collect_sheets()
    codex = collect_codex()
    data = json.dumps({"sheets": sheets, "codex": codex}, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    data = data.replace("</", "<\\/")
    out = Path(a.out)
    out.write_text(PAGE.replace("__DATA__", data), encoding="utf-8")
    variants = sorted({s["variant"] for s in sheets})
    missing = [s["id"] for s in sheets if not s["preview"]]
    print(f"{out}: {len(sheets)} Blätter, Varianten {', '.join(variants)}, Codex-Links {len(codex)}"
          + (f", ohne Vorschau: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
