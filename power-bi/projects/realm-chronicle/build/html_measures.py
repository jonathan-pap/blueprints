"""html_measures - writes _HTML.tmdl, the Intro page's HTML-in-SVG measures, sized to the grid.

Durable on purpose: the panels' pixel size comes from the resolved `intro` layout, so a canvas or
grid change (FHD -> 1280x720 on 2026-09-13) regenerates them instead of leaving stale hardcoded sizes.

Sizing: each panel is DESIGNED at a reference width (1840 for full-width, 896 for half-width) and its
reference height follows the region's proportions. The <svg> then declares the region's real size
with a viewBox of the reference size, so the whole panel scales as one drawing - type, borders and
spacing keep their proportions at any canvas.

TMDL rules (02-build/model/update/dax-multiline.md): declaration depth 1, properties depth 2, body
depth 3; /// docstrings only, never // inside a body; CRLF + tabs. Property order mirrors what Desktop
writes back (displayFolder, lineageTag, dataCategory), and existing lineageTags are reused, so Desktop
keeps each measure's identity and a re-run is byte-identical.
HTML rules (02-build/visuals/svg/html-in-svg.md): xmlns on <svg> AND the inner <div>, single-quoted
attributes, closed tags, numeric entities for symbols, <style> for repeated CSS, SMIL for animation.

Measures live in their own table: the synthetic-data hand-off rewrites _Measures.tmdl on every run.
"""
import io
import os
import re
import uuid

T, CRLF = "\t", "\r\n"


def _existing_tags(path):
    """measure/table/column name -> lineageTag already in the file (keeps Desktop's object identity)."""
    if not os.path.isfile(path):
        return {}
    tags, current = {}, None
    for line in io.open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"^\t?(table|measure|column) ('?)(.+?)\2( =.*)?$", line)
        if m:
            current = m.group(3)
            continue
        t = re.match(r"^\t+lineageTag: (\S+)", line)
        if t and current is not None and current not in tags:
            tags[current] = t.group(1)
    return tags


def _tag(tags, key):
    return tags.get(key) or str(uuid.uuid5(uuid.NAMESPACE_URL, "realm-chronicle/_HTML/" + key))


def _svg_open(w, h, rw, rh):
    return [
        '    "data:image/svg+xml;utf8," &',
        f"    \"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {rw} {rh}'>\" &",
        f"    \"<foreignObject x='0' y='0' width='{rw}' height='{rh}'>\" &",
    ]


def _tidy(e, pattern_one, pattern_whole):
    """A number in a unit, without a meaningless trailing '.0': 900 not 900.0, 2.4 stays 2.4.
    From 100 up in the unit it's whole (137K, not 136.8K) - a decimal there is noise."""
    return (f'IF ( {e} >= 100, FORMAT ( {e}, "{pattern_whole}" ), '
            f'IF ( ROUND ( {e}, 1 ) = INT ( ROUND ( {e}, 1 ) ), FORMAT ( ROUND ( {e}, 1 ), "{pattern_whole}" ), '
            f'FORMAT ( {e}, "{pattern_one}" ) ) )')


def _compact(v):
    """Compact figure: 2.4M, 18M, 900K, 137K, 950. One home for the rule - every panel uses it."""
    return (f'IF ( {v} >= 1000000, {_tidy(v + " / 1000000", "0.0", "0")} & "M", '
            f'IF ( {v} >= 1000, {_tidy(v + " / 1000", "0.0", "0")} & "K", FORMAT ( {v}, "#,0" ) ) )')


def _yoy(m):
    return (f'DIVIDE ( CALCULATE ( {m}, DimDate[Year] = _y1 ) - CALCULATE ( {m}, DimDate[Year] = _y0 ), '
            f'CALCULATE ( {m}, DimDate[Year] = _y0 ) )')


def _chip(g):
    return (f'IF ( ISBLANK ( {g} ), "", IF ( {g} >= 0, "<span class=\'ch\'>&#9650; ", '
            f'"<span class=\'ch dn\'>&#9660; " ) & {_tidy("ABS ( " + g + " ) * 100", "0.0", "0")} & "% vs " & _y0 & "</span>" )')


def hero(w, h):
    rw = 1840
    rh = round(rw * h / w)
    return ("Intro Hero HTML",
            "HTML-in-SVG hero banner for the Intro page: the title, and the four-year saga in one sentence "
            "with inline-coloured figures. ImageUrl measure; host in an Image visual (sourceType imageData).",
            [
     'VAR _slain = [Total MonstersSlain]',
     'VAR _boss = CALCULATE ( [Total MonstersSlain], DimMonster[Kind] = "Boss" )',
     'VAR _bounty = [Total BountyGold]',
     'VAR _trade = [Total GoldVolume]',
     'VAR _realms = COUNTROWS ( DimRealm )',
     'VAR _guilds = DISTINCTCOUNT ( DimAdventurer[Guild] )',
     'VAR _heroes = COUNTROWS ( DimAdventurer )',
     'VAR _y0 = MIN ( DimDate[Year] )',
     'VAR _y1 = MAX ( DimDate[Year] )',
     f'VAR _fSlain = {_compact("_slain")}',
     'VAR _fBoss = FORMAT ( _boss, "#,0" )',
     f'VAR _fBounty = {_compact("_bounty")}',
     f'VAR _fTrade = {_compact("_trade")}',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='h'>\" &",
     '    "<style>" &',
     f'    ".h{{width:{rw}px;height:{rh}px;box-sizing:border-box;position:relative;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5;border-radius:18px;border:2px solid #c9a227;background:radial-gradient(ellipse at 15% 0%,#3d2c10 0%,transparent 55%),radial-gradient(ellipse at 100% 100%,#1c2e4d 0%,transparent 60%),linear-gradient(180deg,#161f31,#0a0f1a);padding:36px 52px}}" &',
     '    ".h .ey{font-size:18px;letter-spacing:6px;text-transform:uppercase;color:#c9a227;display:flex;align-items:center;gap:14px}" &',
     '    ".h .ey i{display:block;width:64px;height:1px;background:#c9a227}" &',
     '    ".h .t{font-family:Georgia,Cambria,serif;font-size:80px;font-weight:700;letter-spacing:10px;line-height:1.05;margin:14px 0 12px;color:#f0cf5e;text-shadow:0 0 28px rgba(232,195,73,0.35),0 3px 0 #5e470f}" &',
     '    ".h .n{font-size:26px;line-height:1.5;color:#b9c6da;max-width:1480px}" &',
     '    ".h b{font-weight:700}.h .k{color:#f4d770}.h .r{color:#ff7b7b}.h .g{color:#6fd49b}.h .m{color:#c9d6ea}" &',
     '    ".h .sw{position:absolute;right:56px;bottom:-54px;font-size:300px;line-height:1;color:#c9a227;opacity:0.07}" &',
     '    "</style>" &',
     "    \"<div class='ey'><i></i>Guilds &#183; Monsters &#183; Quests &#183; Gold<i></i></div>\" &",
     "    \"<div class='t'>THE REALM CHRONICLE</div>\" &",
     "    \"<div class='n'>Across <b class='k'>\" & _realms & \" realms</b>, <b class='m'>\" & _heroes & \" adventurers</b> of \" & _guilds & \" guilds slew <b class='r'>\" & _fSlain & \" monsters</b> &#8212; <b class='r'>\" & _fBoss & \"</b> of them bosses &#8212; claimed <b class='k'>\" & _fBounty & \" gold</b> in bounties, and moved <b class='g'>\" & _fTrade & \" gold</b> through the Grand Exchange. <span class='m'>\" & _y0 & \" &#8211; \" & _y1 & \"</span></div>\" &",
     "    \"<div class='sw'>&#9876;</div>\" &",
     '    "</div></foreignObject>" &',
     f"    \"<circle cx='{rw - 226}' cy='48' r='7' fill='#2ecc71'><animate attributeName='r' values='6;9;6' dur='1.6s' repeatCount='indefinite'/><animate attributeName='opacity' values='1;0.45;1' dur='1.6s' repeatCount='indefinite'/></circle>\" &",
     f"    \"<text x='{rw - 208}' y='54' font-family='Segoe UI,Arial,sans-serif' font-size='16' letter-spacing='2' fill='#8aa0c0'>THE REALM ENDURES</text>\" &",
     '    "</svg>"',
            ])


def _tile(accent, icon, value_var, chip_var, label, sub_expr):
    return (f"    \"<div class='c'><div class='bar' style='background:{accent}'></div><div class='top'><span class='ic'>{icon}</span>\" & {chip_var} & "
            f"\"</div><div class='v' style='color:{accent}'>\" & {value_var} & \"</div><div class='lb'>{label}</div><div class='sb'>\" & {sub_expr} & \"</div></div>\" &")


def ledgers(w, h):
    rw = 1840
    rh = round(rw * h / w)
    return ("Intro Ledgers HTML",
            "HTML-in-SVG strip of four stat tiles, one per fact table (kills, bounties, loot, exchange), each with "
            "a year-over-year chip for the latest year. ImageUrl measure; host in an Image visual.",
            [
     'VAR _y1 = MAX ( DimDate[Year] )',
     'VAR _y0 = _y1 - 1',
     'VAR _k = [Total MonstersSlain]',
     'VAR _b = [Total BountyGold]',
     'VAR _d = [Total DropCount]',
     'VAR _t = [Total GoldVolume]',
     f'VAR _kg = {_yoy("[Total MonstersSlain]")}',
     f'VAR _bg = {_yoy("[Total BountyGold]")}',
     f'VAR _dg = {_yoy("[Total DropCount]")}',
     f'VAR _tg = {_yoy("[Total GoldVolume]")}',
     f'VAR _kv = {_compact("_k")}',
     f'VAR _bv = {_compact("_b")}',
     f'VAR _dv = {_compact("_d")}',
     f'VAR _tv = {_compact("_t")}',
     f'VAR _kc = {_chip("_kg")}',
     f'VAR _bc = {_chip("_bg")}',
     f'VAR _dc = {_chip("_dg")}',
     f'VAR _tc = {_chip("_tg")}',
     'VAR _leg = CALCULATE ( [Total DropCount], DimItem[Rarity] = "Legendary" )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='l'>\" &",
     '    "<style>" &',
     f'    ".l{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:grid;grid-template-columns:repeat(4,1fr);column-gap:26px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     f'    ".l .c{{position:relative;box-sizing:border-box;height:{rh}px;border-radius:14px;background:linear-gradient(180deg,#172136,#0d1422);border:1px solid #2a3953;padding:22px 26px;overflow:hidden}}" &',
     '    ".l .bar{position:absolute;left:0;top:0;right:0;height:5px}" &',
     '    ".l .top{display:flex;align-items:center;justify-content:space-between;height:36px}" &',
     '    ".l .ic{font-size:32px;line-height:1}" &',
     '    ".l .ch{font-size:16px;font-weight:600;padding:4px 11px;border-radius:999px;background:#12301f;color:#6fd49b}" &',
     '    ".l .dn{background:#3a1616;color:#ff7b7b}" &',
     '    ".l .v{font-size:58px;font-weight:700;line-height:1;margin-top:14px;font-variant-numeric:tabular-nums}" &',
     '    ".l .lb{font-size:16px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0;margin-top:10px}" &',
     '    ".l .sb{font-size:18px;color:#b9c6da;margin-top:6px}" &',
     '    "</style>" &',
     _tile("#ff7b7b", "&#9876;",   "_kv", "_kc", "Monsters slain",   'FORMAT ( [Total PartyWipes], "#,0" ) & " party wipes"'),
     _tile("#f4d770", "&#x1F4DC;", "_bv", "_bc", "Gold in bounties", 'FORMAT ( [Total QuestsCompleted], "#,0" ) & " quests completed"'),
     _tile("#c89bff", "&#x1F48E;", "_dv", "_dc", "Loot drops",       'FORMAT ( _leg, "#,0" ) & " legendary"'),
     _tile("#6fd49b", "&#9878;",   "_tv", "_tc", "Gold traded",      'FORMAT ( [Total QuantityTraded], "#,0" ) & " units exchanged"'),
     '    "</div></foreignObject></svg>"',
            ])


def legends(w, h):
    rw = 896
    rh = round(rw * h / w)
    return ("Intro Legends HTML",
            "HTML-in-SVG leaderboard of the top five slayers: rank medal, name, class, guild and rank, kills with a "
            "relative bar. Respects outer filters via ALLSELECTED. ImageUrl measure; host in an Image visual.",
            [
     'VAR _N = 5',
     'VAR _A =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimAdventurer ), DimAdventurer[AdventurerKey], DimAdventurer[Adventurer], DimAdventurer[Guild], DimAdventurer[Class], DimAdventurer[Rank] ),',
     '        "@kills", [Total MonstersSlain]',
     '    )',
     'VAR _Top = TOPN ( _N, FILTER ( _A, [@kills] > 0 ), [@kills], DESC )',
     'VAR _Max = MAXX ( _Top, [@kills] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _Top,',
     '        VAR _pos = RANKX ( _Top, [@kills], , DESC )',
     '        VAR _nm = SUBSTITUTE ( DimAdventurer[Adventurer], "&", "&amp;" )',
     '        VAR _gd = SUBSTITUTE ( DimAdventurer[Guild], "&", "&amp;" )',
     '        VAR _medal = SWITCH ( _pos, 1, "#f4d770", 2, "#cfd8e3", 3, "#d08a4c", "#3a4a66" )',
     '        VAR _ic = SWITCH ( DimAdventurer[Class], "Warrior", "&#9876;", "Mage", "&#10024;", "Rogue", "&#x1F5E1;", "Ranger", "&#x1F3F9;", "Cleric", "&#9877;", "Warden", "&#x1F6E1;", "&#9733;" )',
     '        VAR _pct = INT ( DIVIDE ( [@kills], _Max ) * 100 )',
     '        RETURN',
     "            \"<div class='r'>\" &",
     "            \"<div class='md' style='background:\" & _medal & \"'>\" & _pos & \"</div>\" &",
     "            \"<div><div class='nm'>\" & _nm & \"</div><div class='gd'>\" & _ic & \" \" & DimAdventurer[Class] & \" &#183; \" & _gd & \" &#183; \" & DimAdventurer[Rank] & \"</div></div>\" &",
     "            \"<div><div class='kv'>\" & FORMAT ( [@kills], \"#,0\" ) & \"</div><div class='bb'><span style='width:\" & _pct & \"%'></span></div></div>\" &",
     '            "</div>",',
     '        "",',
     '        [@kills], DESC',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='lg'>\" &",
     '    "<style>" &',
     f'    ".lg{{width:{rw}px;height:{rh}px;box-sizing:border-box;border-radius:16px;border:2px solid #c9a227;background:linear-gradient(180deg,#1b2436,#0d1422);padding:20px 28px 24px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5;display:flex;flex-direction:column}}" &',
     '    ".lg .hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #2c3a52;padding-bottom:10px;margin-bottom:8px}" &',
     '    ".lg .ttl{font-family:Georgia,Cambria,serif;font-size:26px;font-weight:700;letter-spacing:3px;color:#e8c349}" &',
     '    ".lg .sub{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0}" &',
     '    ".lg .r{flex:1;display:grid;grid-template-columns:46px 1fr 250px;align-items:center;column-gap:16px;padding:5px 0;border-bottom:1px solid #1b243a}.lg .r:last-child{border-bottom:none}" &',
     '    ".lg .md{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;color:#0d1422}" &',
     '    ".lg .nm{font-size:18px;font-weight:600}" &',
     '    ".lg .gd{font-size:14px;color:#8aa0c0;margin-top:1px}" &',
     '    ".lg .kv{text-align:right;font-size:20px;font-weight:700;color:#ff8a8a;font-variant-numeric:tabular-nums}" &',
     '    ".lg .bb{height:7px;background:#1f2a3d;border-radius:4px;overflow:hidden;margin-top:6px}" &',
     '    ".lg .bb span{display:block;height:100%;background:linear-gradient(90deg,#b8322f,#ff8a8a)}" &',
     '    "</style>" &',
     "    \"<div class='hd'><div class='ttl'>&#9819; HALL OF LEGENDS</div><div class='sub'>Top slayers &#183; all time</div></div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
            ])


def bosses(w, h):
    rw = 896
    rh = round(rw * h / w)
    return ("Intro Bosses HTML",
            "HTML-in-SVG roll of the four raid bosses: kills, and deadliness as party wipes per 1,000 kills with a "
            "relative bar, accented by habitat. ImageUrl measure; host in an Image visual.",
            [
     'VAR _B =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( FILTER ( ALLSELECTED ( DimMonster ), DimMonster[Kind] = "Boss" ), DimMonster[MonsterKey], DimMonster[Monster], DimMonster[Family], DimMonster[Habitat] ),',
     '        "@kills", [Total MonstersSlain],',
     '        "@wipes", [Total PartyWipes]',
     '    )',
     'VAR _MaxRate = MAXX ( _B, DIVIDE ( [@wipes], [@kills] ) )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _B,',
     '        VAR _nm = SUBSTITUTE ( DimMonster[Monster], "&", "&amp;" )',
     '        VAR _ic = SWITCH ( DimMonster[Monster], "Emberfang the Wyrm", "&#x1F409;", "Vorrak, Hollow Crown", "&#x1F608;", "Glacius Rimeheart", "&#x1F432;", "The Verdant Maw", "&#x1F40A;", "&#9760;" )',
     '        VAR _acc = SWITCH ( DimMonster[Habitat], "Emberwaste", "#ff7a45", "Hollowmere", "#b98cff", "Frosthollow", "#7cc8ff", "Verdant Deep", "#5fd48a", "#ff6b6b" )',
     '        VAR _rate = DIVIDE ( [@wipes], [@kills] ) * 1000',
     '        VAR _pct = INT ( DIVIDE ( DIVIDE ( [@wipes], [@kills] ), _MaxRate ) * 100 )',
     '        RETURN',
     "            \"<div class='b' style='border-left:4px solid \" & _acc & \"'>\" &",
     "            \"<div class='ic'>\" & _ic & \"</div>\" &",
     "            \"<div><div class='nm' style='color:\" & _acc & \"'>\" & _nm & \"</div><div class='mt'>\" & DimMonster[Family] & \" &#183; \" & DimMonster[Habitat] & \"</div></div>\" &",
     "            \"<div><div class='kv'>\" & FORMAT ( [@kills], \"#,0\" ) & \"<span class='u'> slain</span></div>\" &",
     "            \"<div class='dl'>\" & FORMAT ( _rate, \"0.0\" ) & \" wipes per 1k</div>\" &",
     "            \"<div class='bb'><span style='width:\" & _pct & \"%;background:\" & _acc & \"'></span></div></div>\" &",
     '            "</div>",',
     '        "",',
     '        [@kills], DESC',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='bs'>\" &",
     '    "<style>" &',
     f'    ".bs{{width:{rw}px;height:{rh}px;box-sizing:border-box;border-radius:16px;border:2px solid #7a2a2a;background:linear-gradient(180deg,#221521,#0e0c16);padding:20px 28px 24px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5;display:flex;flex-direction:column}}" &',
     '    ".bs .hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #3a2436;padding-bottom:10px;margin-bottom:8px}" &',
     '    ".bs .ttl{font-family:Georgia,Cambria,serif;font-size:26px;font-weight:700;letter-spacing:3px;color:#ff7a6b}" &',
     '    ".bs .sub{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#a58aa0}" &',
     '    ".bs .b{flex:1;display:grid;grid-template-columns:54px 1fr 240px;align-items:center;column-gap:14px;padding:9px 14px;margin-bottom:9px;background:rgba(255,255,255,0.03);border-radius:8px}" &',
     '    ".bs .b:last-child{margin-bottom:0}.bs .ic{font-size:36px;line-height:1;text-align:center}" &',
     '    ".bs .nm{font-size:20px;font-weight:700}" &',
     '    ".bs .mt{font-size:15px;color:#a58aa0;margin-top:2px}" &',
     '    ".bs .kv{text-align:right;font-size:20px;font-weight:700;font-variant-numeric:tabular-nums}" &',
     '    ".bs .kv .u{font-size:14px;font-weight:400;color:#a58aa0}" &',
     '    ".bs .dl{text-align:right;font-size:14px;color:#c9a9c4;margin-top:2px}" &',
     '    ".bs .bb{height:7px;background:#2a1f2c;border-radius:4px;overflow:hidden;margin-top:5px}" &',
     '    ".bs .bb span{display:block;height:100%}" &',
     '    "</style>" &',
     "    \"<div class='hd'><div class='ttl'>&#9760; THE BOSS ROLL</div><div class='sub'>Raid targets &#183; deadliness</div></div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
            ])


# ---- Bestiary ----------------------------------------------------------------------------------

DATASET = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "..", "..", "synthetic-data", "outputs",
                                        "realm-chronicle", "latest"))

HABITAT_ACCENT = {"Emberwaste": "#ff7a45", "Hollowmere": "#b98cff", "Thornveil": "#7fd08a",
                  "Saltreach": "#5cc8d6", "Gloamspire": "#8f9dff", "Frosthollow": "#7cc8ff",
                  "Ashfall Reach": "#d9a066", "Verdant Deep": "#5fd48a"}
FAMILY_ICON = {"Beast": 0x1F43A, "Undead": 0x1F480, "Dragon": 0x1F409,
               "Elemental": 0x1F525, "Demon": 0x1F608, "Construct": 0x1F5FF}


def _switch(column, mapping, default):
    parts = ", ".join('"%s", "%s"' % (k.replace('"', '""'), v) for k, v in mapping.items())
    return 'SWITCH ( %s, %s, "%s" )' % (column, parts, default)


def _monster_icons():
    """Monster -> numeric entity, read from the dataset's Icon column so the dataset stays the single
    source. Python's ord() handles emoji above U+FFFF; DAX UNICODE() can return half a surrogate pair
    there, and an invalid entity silently breaks the whole SVG."""
    import csv
    with io.open(os.path.join(DATASET, "DimMonster.csv"), encoding="utf-8", newline="") as f:
        return {r["Monster"]: "&#x%X;" % ord(r["Icon"][0]) for r in csv.DictReader(f)}


def _pill(var, colour, label):
    return (f"    \"<div class='k'><div class='v' style='color:{colour}'>\" & {var} & \"</div>"
            f"<div class='l'><i style='background:{colour}'></i>{label}</div></div>\" &")


def page_header(w, h, measure, desc, eyebrow, title, var_lines, pills):
    """The header band every inner page shares: eyebrow + serif title on the left, four stat pills on
    the right. pills: [(dax_expression, colour, label), ...]."""
    rw = 1840
    rh = round(rw * h / w)
    return (measure, desc, [
     *var_lines,
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='hb'>\" &",
     '    "<style>" &',
     f'    ".hb{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;padding:0 44px;border-radius:16px;border:2px solid #c9a227;background:radial-gradient(ellipse at 10% 0%,#3d2c10 0%,transparent 60%),linear-gradient(180deg,#161f31,#0a0f1a);font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".hb .ey{font-size:16px;letter-spacing:5px;text-transform:uppercase;color:#c9a227}" &',
     '    ".hb .t{font-family:Georgia,Cambria,serif;font-size:60px;font-weight:700;letter-spacing:8px;line-height:1.05;color:#f0cf5e;text-shadow:0 0 24px rgba(232,195,73,0.3),0 3px 0 #5e470f;margin-top:4px}" &',
     '    ".hb .ks{display:flex;gap:16px}" &',
     '    ".hb .k{box-sizing:border-box;min-width:180px;padding:14px 20px;border-radius:12px;background:rgba(255,255,255,0.04);border:1px solid #2a3953}" &',
     '    ".hb .v{font-size:34px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums;white-space:nowrap}" &',
     '    ".hb .l{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0;margin-top:7px}" &',
     '    ".hb .l i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px}" &',
     '    "</style>" &',
     f"    \"<div><div class='ey'>{eyebrow}</div><div class='t'>{title}</div></div>\" &",
     "    \"<div class='ks'>\" &",
     *[_pill(expr, colour, label) for expr, colour, label in pills],
     '    "</div></div></foreignObject></svg>"',
    ])


def bestiary_header(w, h):
    return page_header(
        w, h, "Bestiary Header HTML",
        "HTML-in-SVG header for the Bestiary page: the title, and monster kills split by kind (Field, Elite, "
        "Boss) with the number of creatures catalogued. ImageUrl measure; host in an Image visual.",
        "The Hunt &#183; a field guide to the realm", "THE BESTIARY",
        ['VAR _f = CALCULATE ( [Total MonstersSlain], DimMonster[Kind] = "Field" )',
         'VAR _e = CALCULATE ( [Total MonstersSlain], DimMonster[Kind] = "Elite" )',
         'VAR _b = CALCULATE ( [Total MonstersSlain], DimMonster[Kind] = "Boss" )',
         'VAR _n = COUNTROWS ( DimMonster )'],
        [(_compact("_f"), "#8fcf97", "Field slain"),
         (_compact("_e"), "#c89bff", "Elite slain"),
         (_compact("_b"), "#ff7b7b", "Boss slain"),
         ("_n", "#e8c349", "Creatures")])


def _cards(kind, css_class, icons):
    return [
     f'VAR _{css_class} =',
     '    CONCATENATEX (',
     f'        FILTER ( _M, DimMonster[Kind] = "{kind}" ),',
     '        VAR _nm = SUBSTITUTE ( DimMonster[Monster], "&", "&amp;" )',
     f'        VAR _ic = {_switch("DimMonster[Monster]", icons, "&#9760;")}',
     f'        VAR _acc = {_switch("DimMonster[Habitat]", HABITAT_ACCENT, "#8aa0c0")}',
     '        VAR _rate = DIVIDE ( [@wipes], [@kills] ) * 1000',
     '        RETURN',
     f"            \"<div class='cd {css_class}' style='border-left-color:\" & _acc & \"'>\" &",
     "            \"<div class='ic'>\" & _ic & \"</div>\" &",
     "            \"<div class='bd'><div class='nm' style='color:\" & _acc & \"'>\" & _nm & \"</div>\" &",
     "            \"<div class='mt'>\" & DimMonster[Family] & \" &#183; \" & DimMonster[Habitat] & \"</div>\" &",
     "            \"<div class='ft'><span class='st'>\" & REPT ( \"&#9733;\", DimMonster[Tier] ) & \"</span>\" &",
     "            \"<span class='kv'>\" & FORMAT ( [@kills], \"#,0\" ) & \"<span class='u'> slain</span><span class='dl'> &#183; \" & FORMAT ( _rate, \"0.0\" ) & \"/1k</span></span></div></div>\" &",
     '            "</div>",',
     '        "",',
     '        [@kills], DESC',
     '    )',
    ]


def _section(label, var, kind, cols):
    return [
     f"    \"<div class='sh'><span>{label}</span><i></i><b>\" & COUNTROWS ( FILTER ( _M, DimMonster[Kind] = \"{kind}\" ) ) & \"</b></div>\" &",
     f"    \"<div class='row r{cols}'>\" & {var} & \"</div>\" &"]


def bestiary_creatures(w, h):
    rw = 1400
    rh = round(rw * h / w)
    icons = _monster_icons()
    return ("Bestiary Creatures HTML",
            "HTML-in-SVG field guide: all creatures as cards grouped Boss, Elite, Field, each with family, habitat, "
            "tier, kills and party wipes per 1,000 kills, ordered by kills. ImageUrl measure; host in an Image visual.",
            [
     'VAR _M =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimMonster ), DimMonster[MonsterKey], DimMonster[Monster], DimMonster[Kind], DimMonster[Family], DimMonster[Tier], DimMonster[Habitat] ),',
     '        "@kills", [Total MonstersSlain],',
     '        "@wipes", [Total PartyWipes]',
     '    )',
     *_cards("Boss", "boss", icons),
     *_cards("Elite", "elite", icons),
     *_cards("Field", "field", icons),
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='bg'>\" &",
     '    "<style>" &',
     f'    ".bg{{width:{rw}px;height:{rh}px;box-sizing:border-box;border-radius:16px;border:1px solid #2a3953;background:linear-gradient(180deg,#141d2f,#0c1220);padding:18px 20px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5;overflow:hidden}}" &',
     '    ".bg .sh{display:flex;align-items:center;gap:12px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#8aa0c0;margin:2px 0 8px}" &',
     '    ".bg .sh i{flex:1;height:1px;background:#2a3953}" &',
     '    ".bg .sh b{font-weight:600;color:#c9d6ea;letter-spacing:1px}" &',
     '    ".bg .row{display:grid;gap:10px;margin-bottom:12px}" &',
     '    ".bg .r4{grid-template-columns:repeat(4,1fr)}.bg .r5{grid-template-columns:repeat(5,1fr)}" &',
     '    ".bg .cd{display:grid;grid-template-columns:auto 1fr;align-items:center;column-gap:12px;box-sizing:border-box;border-radius:10px;background:rgba(255,255,255,0.035);border:1px solid #243149;border-left-width:3px;padding:0 14px;overflow:hidden}" &',
     '    ".bg .boss{height:132px}.bg .elite{height:96px}.bg .field{height:84px}" &',
     '    ".bg .ic{line-height:1;text-align:center}.bg .boss .ic{font-size:44px}.bg .elite .ic{font-size:32px}.bg .field .ic{font-size:28px}" &',
     '    ".bg .bd{min-width:0}" &',
     '    ".bg .nm{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" &',
     '    ".bg .boss .nm{font-size:19px}.bg .elite .nm{font-size:16px}.bg .field .nm{font-size:15px;font-weight:600}" &',
     '    ".bg .mt{font-size:12px;color:#8aa0c0;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" &',
     '    ".bg .ft{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-top:5px}" &',
     '    ".bg .st{font-size:11px;color:#c9a227;letter-spacing:1px;white-space:nowrap}" &',
     '    ".bg .kv{font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}.bg .boss .kv{font-size:18px}.bg .elite .kv{font-size:15px}.bg .field .kv{font-size:14px}" &',
     '    ".bg .kv .u{font-weight:400;font-size:12px;color:#8aa0c0}.bg .kv .dl{font-weight:400;font-size:12px;color:#c9a9c4}" &',
     '    "</style>" &',
     *_section("Bosses", "_boss", "Boss", 4),
     *_section("Elites", "_elite", "Elite", 4),
     *_section("Field creatures", "_field", "Field", 5),
     '    "</div></foreignObject></svg>"',
            ])


def bestiary_families(w, h):
    rw = 560
    rh = round(rw * h / w)
    fam_icons = {k: "&#x%X;" % v for k, v in FAMILY_ICON.items()}
    return ("Bestiary Families HTML",
            "HTML-in-SVG column of the six monster families: share of kills with a relative bar, kills and party "
            "wipes per 1,000 kills, then the single deadliest creature. ImageUrl measure; host in an Image visual.",
            [
     'VAR _F =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimMonster ), DimMonster[Family] ),',
     '        "@kills", [Total MonstersSlain],',
     '        "@wipes", [Total PartyWipes]',
     '    )',
     'VAR _Tot = SUMX ( _F, [@kills] )',
     'VAR _Max = MAXX ( _F, [@kills] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _F,',
     f'        VAR _ic = {_switch("DimMonster[Family]", fam_icons, "&#9733;")}',
     '        VAR _pct = INT ( DIVIDE ( [@kills], _Max ) * 100 )',
     '        VAR _rate = DIVIDE ( [@wipes], [@kills] ) * 1000',
     '        RETURN',
     "            \"<div class='f'><div class='fh'><span class='ic'>\" & _ic & \"</span><span class='fn'>\" & DimMonster[Family] & \"</span><span class='sh'>\" & FORMAT ( DIVIDE ( [@kills], _Tot ), \"0%\" ) & \"</span></div>\" &",
     "            \"<div class='bb'><span style='width:\" & _pct & \"%'></span></div>\" &",
     "            \"<div class='fm'>\" & FORMAT ( [@kills], \"#,0\" ) & \" slain &#183; \" & FORMAT ( _rate, \"0.0\" ) & \" wipes/1k</div></div>\",",
     '        "",',
     '        [@kills], DESC',
     '    )',
     'VAR _D =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimMonster ), DimMonster[Monster], DimMonster[Kind], DimMonster[Habitat] ),',
     '        "@rate", DIVIDE ( [Total PartyWipes], [Total MonstersSlain] ) * 1000',
     '    )',
     'VAR _Top = TOPN ( 1, _D, [@rate], DESC )',
     'VAR _dName = SUBSTITUTE ( MAXX ( _Top, DimMonster[Monster] ), "&", "&amp;" )',
     'VAR _dMeta = MAXX ( _Top, DimMonster[Kind] ) & " &#183; " & MAXX ( _Top, DimMonster[Habitat] )',
     'VAR _dRate = FORMAT ( MAXX ( _Top, [@rate] ), "0.0" )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='fa'>\" &",
     '    "<style>" &',
     f'    ".fa{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;flex-direction:column;border-radius:16px;border:1px solid #2a3953;background:linear-gradient(180deg,#141d2f,#0c1220);padding:26px 30px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".fa .hd{font-family:Georgia,Cambria,serif;font-size:30px;font-weight:700;letter-spacing:3px;color:#e8c349;border-bottom:1px solid #2c3a52;padding-bottom:12px;margin-bottom:6px}" &',
     '    ".fa .f{padding:15px 0;border-bottom:1px solid #1b243a}" &',
     '    ".fa .fh{display:flex;align-items:center;gap:12px}" &',
     '    ".fa .ic{font-size:30px;line-height:1}" &',
     '    ".fa .fn{flex:1;font-size:24px;font-weight:600}" &',
     '    ".fa .sh{font-size:24px;font-weight:700;color:#f4d770;font-variant-numeric:tabular-nums}" &',
     '    ".fa .bb{height:9px;background:#1f2a3d;border-radius:5px;overflow:hidden;margin-top:10px}" &',
     '    ".fa .bb span{display:block;height:100%;background:linear-gradient(90deg,#9a7a1c,#f4d770)}" &',
     '    ".fa .fm{font-size:18px;color:#8aa0c0;margin-top:8px;font-variant-numeric:tabular-nums}" &',
     '    ".fa .dd{margin-top:auto;border-radius:12px;border:1px solid #7a2a2a;background:linear-gradient(180deg,#2a1520,#170d16);padding:20px 22px}" &',
     '    ".fa .dd .lb{font-size:15px;letter-spacing:3px;text-transform:uppercase;color:#ff7a6b}" &',
     '    ".fa .dd .nm{font-size:28px;font-weight:700;margin-top:8px}" &',
     '    ".fa .dd .mt{font-size:18px;color:#a58aa0;margin-top:4px}" &',
     '    ".fa .dd .rt{font-size:22px;font-weight:700;color:#ff8a8a;margin-top:10px}" &',
     '    "</style>" &',
     "    \"<div class='hd'>BY FAMILY</div>\" &",
     '    _Rows &',
     "    \"<div class='dd'><div class='lb'>&#9760; Deadliest creature</div><div class='nm'>\" & _dName & \"</div><div class='mt'>\" & _dMeta & \"</div><div class='rt'>\" & _dRate & \" wipes per 1k kills</div></div>\" &",
     '    "</div></foreignObject></svg>"',
            ])


# ---- shared: a ranked bar list (danger, rank, category, rarity) --------------------------------

def bar_panel(w, h, measure, desc, title, subtitle, table, columns, label, colour, value, value_unit,
              extra, extra_unit, order_by, order_dir, border="#2a3953"):
    """A titled list of bars, one per member: label with a colour dot, compact value, a relative bar,
    and a meta line (share of total + a second measure). Rows share the panel height."""
    rw = 896 if w > 450 else 560
    rh = round(rw * h / w)
    return (measure, desc, [
     'VAR _T =',
     '    ADDCOLUMNS (',
     f'        SUMMARIZE ( ALLSELECTED ( {table} ), {", ".join(columns)} ),',
     f'        "@v", {value},',
     f'        "@x", {extra}',
     '    )',
     'VAR _Tot = SUMX ( _T, [@v] )',
     'VAR _Max = MAXX ( _T, [@v] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _T,',
     f'        VAR _c = {colour}',
     '        VAR _pct = INT ( DIVIDE ( [@v], _Max ) * 100 )',
     '        RETURN',
     f"            \"<div class='r'><div class='rh'><span class='nm'><i style='background:\" & _c & \"'></i>\" & {label} & \"</span><span class='v'>\" & {_compact('[@v]')} & \"<span class='u'>{value_unit}</span></span></div>\" &",
     "            \"<div class='bb'><span style='width:\" & _pct & \"%;background:\" & _c & \"'></span></div>\" &",
     f"            \"<div class='m'>\" & {_tidy('DIVIDE ( [@v], _Tot ) * 100', '0.0', '0')} & \"% of total &#183; \" & {_compact('[@x]')} & \"{extra_unit}</div></div>\",",
     '        "",',
     f'        {order_by}, {order_dir}',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='bp'>\" &",
     '    "<style>" &',
     f'    ".bp{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;flex-direction:column;border-radius:16px;border:1px solid {border};background:linear-gradient(180deg,#141d2f,#0c1220);padding:20px 28px 22px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".bp .hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #2c3a52;padding-bottom:10px;margin-bottom:4px}" &',
     '    ".bp .ttl{font-family:Georgia,Cambria,serif;font-size:26px;font-weight:700;letter-spacing:3px;color:#e8c349}" &',
     '    ".bp .sub{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0}" &',
     '    ".bp .r{flex:1;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #1b243a}.bp .r:last-child{border-bottom:none}" &',
     '    ".bp .rh{display:flex;align-items:baseline;justify-content:space-between}" &',
     '    ".bp .nm{font-size:20px;font-weight:600}.bp .nm i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:10px}" &',
     '    ".bp .v{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums}.bp .u{font-size:14px;font-weight:400;color:#8aa0c0}" &',
     '    ".bp .bb{height:8px;background:#1f2a3d;border-radius:5px;overflow:hidden;margin-top:7px}.bp .bb span{display:block;height:100%}" &',
     '    ".bp .m{font-size:15px;color:#8aa0c0;margin-top:5px;font-variant-numeric:tabular-nums}" &',
     '    "</style>" &',
     f"    \"<div class='hd'><div class='ttl'>{title}</div><div class='sub'>{subtitle}</div></div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
    ])


def _dataset_icons(table, key):
    import csv
    with io.open(os.path.join(DATASET, table + ".csv"), encoding="utf-8", newline="") as f:
        return {r[key]: "&#x%X;" % ord(r["Icon"][0]) for r in csv.DictReader(f)}


RANK_COLOUR = {"Gold": "#f4d770", "Silver": "#cfd8e3", "Bronze": "#d08a4c", "Copper": "#b87333"}
CATEGORY_COLOUR = {"Weapon": "#ff7b7b", "Armour": "#7cc8ff", "Potion": "#6fd49b",
                   "Reagent": "#c89bff", "Trophy": "#f4d770"}
THREAT_COLOUR = {"Medium": "#f2c037", "High": "#f97316", "Extreme": "#ff5a5a"}


# ---- Quest Board -------------------------------------------------------------------------------

def quests_header(w, h):
    return page_header(
        w, h, "Quests Header HTML",
        "HTML-in-SVG header for the Quest Board: bounty gold, quests completed, gold per quest and days per "
        "quest. ImageUrl measure; host in an Image visual.",
        "Guild contracts &#183; what the realm pays for", "THE QUEST BOARD",
        ['VAR _b = [Total BountyGold]',
         'VAR _q = [Total QuestsCompleted]',
         'VAR _days = DIVIDE ( [Total DaysOnQuest], _q )'],
        [(_compact("_b"), "#f4d770", "Bounty gold"),
         (_compact("_q"), "#6fd49b", "Quests done"),
         ('FORMAT ( DIVIDE ( _b, _q ), "#,0" )', "#e8c349", "Gold per quest"),
         (_tidy("_days", "0.0", "0"), "#7cc8ff", "Days per quest")])


def quest_chains(w, h):
    rw = 1300
    rh = round(rw * h / w)
    return ("Quests Chains HTML",
            "HTML-in-SVG view of the quest chains: each chain as a row of its quests in prerequisite order, with "
            "danger, type, bounty and a relative bar. Chains ordered by total bounty. ImageUrl measure; Image visual.",
            [
     'VAR _C =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimQuest ), DimQuest[ChainName] ),',
     '        "@bounty", [Total BountyGold]',
     '    )',
     'VAR _Max = MAXX ( ALLSELECTED ( DimQuest ), [Total BountyGold] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _C,',
     '        VAR _chain = DimQuest[ChainName]',
     '        VAR _steps = FILTER ( ALLSELECTED ( DimQuest ), DimQuest[ChainName] = _chain )',
     '        VAR _n = COUNTROWS ( _steps )',
     '        VAR _cards =',
     '            CONCATENATEX (',
     '                _steps,',
     '                VAR _bq = [Total BountyGold]',
     '                VAR _pct = INT ( DIVIDE ( _bq, _Max ) * 100 )',
     '                RETURN',
     "                    \"<div class='q'><div class='qt'><i style='background:\" & DimQuest[DangerColor] & \"'></i>\" & DimQuest[Danger] & \" &#183; \" & DimQuest[QuestType] & \"</div>\" &",
     "                    \"<div class='qn'>\" & SUBSTITUTE ( DimQuest[Quest], \"&\", \"&amp;\" ) & \"</div>\" &",
     f"                    \"<div class='qb'>\" & {_compact('_bq')} & \" gold</div>\" &",
     "                    \"<div class='bb'><span style='width:\" & _pct & \"%;background:\" & DimQuest[DangerColor] & \"'></span></div></div>\",",
     "                \"<div class='ar'>&#9656;</div>\",",
     '                DimQuest[ChainStep], ASC',
     '            )',
     '        RETURN',
     f"            \"<div class='ch'><div><div class='cn'>\" & SUBSTITUTE ( _chain, \"&\", \"&amp;\" ) & \"</div><div class='cm'>\" & _n & IF ( _n = 1, \" quest\", \" quests\" ) & \" &#183; \" & {_compact('[@bounty]')} & \" gold</div></div><div class='cs'>\" & _cards & \"</div></div>\",",
     '        "",',
     '        [@bounty], DESC',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='qc'>\" &",
     '    "<style>" &',
     f'    ".qc{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;flex-direction:column;border-radius:16px;border:1px solid #2a3953;background:linear-gradient(180deg,#141d2f,#0c1220);padding:22px 26px 20px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".qc .hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #2c3a52;padding-bottom:10px;margin-bottom:4px}" &',
     '    ".qc .ttl{font-family:Georgia,Cambria,serif;font-size:28px;font-weight:700;letter-spacing:3px;color:#e8c349}" &',
     '    ".qc .sub{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0}" &',
     '    ".qc .ch{flex:1;display:grid;grid-template-columns:200px 1fr;align-items:center;column-gap:16px;border-bottom:1px solid #1b243a}.qc .ch:last-child{border-bottom:none}" &',
     '    ".qc .cn{font-family:Georgia,Cambria,serif;font-size:19px;font-weight:700;color:#f0cf5e}" &',
     '    ".qc .cm{font-size:13px;color:#8aa0c0;margin-top:3px}" &',
     '    ".qc .cs{display:flex;align-items:center;gap:6px}" &',
     '    ".qc .q{flex:0 0 228px;box-sizing:border-box;border-radius:9px;background:rgba(255,255,255,0.035);border:1px solid #243149;padding:8px 11px}" &',
     '    ".qc .qt{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#8aa0c0;display:flex;align-items:center;gap:6px;white-space:nowrap}" &',
     '    ".qc .qt i{display:inline-block;width:8px;height:8px;border-radius:50%}" &',
     '    ".qc .qn{font-size:14px;font-weight:600;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" &',
     '    ".qc .qb{font-size:13px;color:#f4d770;margin-top:3px;font-variant-numeric:tabular-nums}" &',
     '    ".qc .bb{height:4px;background:#1f2a3d;border-radius:3px;overflow:hidden;margin-top:5px}.qc .bb span{display:block;height:100%}" &',
     '    ".qc .ar{color:#8aa0c0;font-size:22px;line-height:1}" &',
     '    "</style>" &',
     "    \"<div class='hd'><div class='ttl'>QUEST CHAINS</div><div class='sub'>Each quest unlocks the next</div></div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
            ])


def quest_danger(w, h):
    return bar_panel(
        w, h, "Quests Danger HTML",
        "HTML-in-SVG bars of bounty gold by quest danger, Low to Extreme, with share and quests completed. "
        "ImageUrl measure; host in an Image visual.",
        "BY DANGER", "Risk sets the price", "DimQuest",
        ["DimQuest[Danger]", "DimQuest[DangerOrder]", "DimQuest[DangerColor]"],
        "DimQuest[Danger]", "DimQuest[DangerColor]",
        "[Total BountyGold]", " gold", "[Total QuestsCompleted]", " quests",
        "DimQuest[DangerOrder]", "ASC")


def quest_rank(w, h):
    return bar_panel(
        w, h, "Quests Rank HTML",
        "HTML-in-SVG bars of bounty gold by adventurer rank, Gold to Copper, with share and quests completed. "
        "ImageUrl measure; host in an Image visual.",
        "BY RANK", "Who takes the contracts", "DimAdventurer",
        ["DimAdventurer[Rank]", "DimAdventurer[RankOrder]"],
        "DimAdventurer[Rank]", _switch("DimAdventurer[Rank]", RANK_COLOUR, "#8aa0c0"),
        "[Total BountyGold]", " gold", "[Total QuestsCompleted]", " quests",
        "DimAdventurer[RankOrder]", "DESC")


# ---- The Exchange ------------------------------------------------------------------------------

def exchange_header(w, h):
    return page_header(
        w, h, "Exchange Header HTML",
        "HTML-in-SVG header for The Exchange: gold traded, units exchanged, gold per unit and legendary loot "
        "drops. ImageUrl measure; host in an Image visual.",
        "Trading posts of the realm &#183; the grand exchange", "THE EXCHANGE",
        ['VAR _g = [Total GoldVolume]',
         'VAR _u = [Total QuantityTraded]',
         'VAR _leg = CALCULATE ( [Total DropCount], DimItem[Rarity] = "Legendary" )'],
        [(_compact("_g"), "#6fd49b", "Gold traded"),
         (_compact("_u"), "#7cc8ff", "Units traded"),
         ('FORMAT ( DIVIDE ( _g, _u ), "#,0" )', "#e8c349", "Gold per unit"),
         (_compact("_leg"), "#F59E0B", "Legendary drops")])


def market_board(w, h):
    rw = 896
    rh = round(rw * h / w)
    icons = _dataset_icons("DimItem", "Item")
    return ("Exchange Board HTML",
            "HTML-in-SVG market board: the twelve items with the most gold traded, rarity-coloured, with category, "
            "units and a relative bar. Respects outer filters via ALLSELECTED. ImageUrl measure; Image visual.",
            [
     'VAR _I =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimItem ), DimItem[ItemKey], DimItem[Item], DimItem[Category], DimItem[Rarity], DimItem[RarityColor] ),',
     '        "@g", [Total GoldVolume],',
     '        "@u", [Total QuantityTraded]',
     '    )',
     'VAR _Top = TOPN ( 12, FILTER ( _I, [@g] > 0 ), [@g], DESC )',
     'VAR _Max = MAXX ( _Top, [@g] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _Top,',
     '        VAR _pos = RANKX ( _Top, [@g], , DESC )',
     f'        VAR _ic = {_switch("DimItem[Item]", icons, "&#9733;")}',
     '        VAR _pct = INT ( DIVIDE ( [@g], _Max ) * 100 )',
     '        RETURN',
     "            \"<div class='r'><div class='ps'>\" & _pos & \"</div><div class='ic'>\" & _ic & \"</div>\" &",
     "            \"<div class='who'><div class='nm' style='color:\" & DimItem[RarityColor] & \"'>\" & SUBSTITUTE ( DimItem[Item], \"&\", \"&amp;\" ) & \"</div><div class='mt'>\" & DimItem[Rarity] & \" &#183; \" & DimItem[Category] & \"</div></div>\" &",
     f"            \"<div class='nu'><div class='kv'>\" & {_compact('[@g]')} & \"<span class='u'> gold</span></div><div class='bb'><span style='width:\" & _pct & \"%'></span></div><div class='mt'>\" & FORMAT ( [@u], \"#,0\" ) & \" units</div></div></div>\",",
     '        "",',
     '        [@g], DESC',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='mb'>\" &",
     '    "<style>" &',
     f'    ".mb{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;flex-direction:column;border-radius:16px;border:2px solid #c9a227;background:linear-gradient(180deg,#1b2436,#0d1422);padding:20px 28px 22px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".mb .hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #2c3a52;padding-bottom:10px;margin-bottom:4px}" &',
     '    ".mb .ttl{font-family:Georgia,Cambria,serif;font-size:26px;font-weight:700;letter-spacing:3px;color:#e8c349}" &',
     '    ".mb .sub{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#8aa0c0}" &',
     '    ".mb .r{flex:1;display:grid;grid-template-columns:30px 40px 1fr 230px;align-items:center;column-gap:12px;border-bottom:1px solid #1b243a}.mb .r:last-child{border-bottom:none}" &',
     '    ".mb .ps{font-size:15px;font-weight:700;color:#56688a;text-align:right;font-variant-numeric:tabular-nums}" &',
     '    ".mb .ic{font-size:26px;line-height:1;text-align:center}" &',
     '    ".mb .nm{font-size:18px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" &',
     '    ".mb .mt{font-size:13px;color:#8aa0c0;margin-top:1px}" &',
     '    ".mb .nu{text-align:right}.mb .kv{font-size:18px;font-weight:700;color:#6fd49b;font-variant-numeric:tabular-nums}.mb .u{font-size:13px;font-weight:400;color:#8aa0c0}" &',
     '    ".mb .bb{height:5px;background:#1f2a3d;border-radius:3px;overflow:hidden;margin:4px 0 2px}.mb .bb span{display:block;height:100%;background:linear-gradient(90deg,#2f7a52,#6fd49b)}" &',
     '    "</style>" &',
     "    \"<div class='hd'><div class='ttl'>&#9878; MARKET BOARD</div><div class='sub'>Most gold traded</div></div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
            ])


def exchange_category(w, h):
    return bar_panel(
        w, h, "Exchange Category HTML",
        "HTML-in-SVG bars of gold traded by item category, with share and units traded. ImageUrl measure; "
        "host in an Image visual.",
        "BY CATEGORY", "Where the gold goes", "DimItem",
        ["DimItem[Category]"],
        "DimItem[Category]", _switch("DimItem[Category]", CATEGORY_COLOUR, "#8aa0c0"),
        "[Total GoldVolume]", " gold", "[Total QuantityTraded]", " units",
        "[@v]", "DESC")


def exchange_rarity(w, h):
    return bar_panel(
        w, h, "Exchange Rarity HTML",
        "HTML-in-SVG bars of loot drops by rarity, Common to Legendary, with share and the gold value of what "
        "dropped - the loot that feeds the exchange. ImageUrl measure; host in an Image visual.",
        "LOOT BY RARITY", "What falls before it trades", "DimItem",
        ["DimItem[Rarity]", "DimItem[RarityOrder]", "DimItem[RarityColor]"],
        "DimItem[Rarity]", "DimItem[RarityColor]",
        "[Total DropCount]", " drops", "[Total LootGoldValue]", " gold value",
        "DimItem[RarityOrder]", "ASC")


# ---- Realm Map ---------------------------------------------------------------------------------

def realms_header(w, h):
    return page_header(
        w, h, "Realms Header HTML",
        "HTML-in-SVG header for the Realm Map: number of realms and regions, the busiest trading post and how "
        "many realms carry an Extreme threat. ImageUrl measure; host in an Image visual.",
        "Eight realms &#183; four regions &#183; one chronicle", "THE REALM MAP",
        ['VAR _n = COUNTROWS ( DimRealm )',
         'VAR _reg = DISTINCTCOUNT ( DimRealm[Region] )',
         'VAR _top = MAXX ( TOPN ( 1, ADDCOLUMNS ( VALUES ( DimRealm[Realm] ), "@g", [Total GoldVolume] ), [@g], DESC ), DimRealm[Realm] )',
         'VAR _ext = CALCULATE ( COUNTROWS ( DimRealm ), DimRealm[ThreatBand] = "Extreme" )'],
        [("_n", "#e8c349", "Realms"),
         ("_reg", "#7cc8ff", "Regions"),
         ("_top", "#6fd49b", "Busiest post"),
         ("_ext", "#ff5a5a", "Extreme threat")])


def realm_map(w, h):
    """Pure SVG - no foreignObject - so the map survives PDF/PowerPoint export."""
    rw = 1000
    rh = round(rw * h / w)
    L, R, TOP, BOT = 130, 130, 90, 140          # plot margins inside the drawing, room for labels
    pw, ph = rw - L - R, rh - TOP - BOT
    return ("Realms Map HTML",
            "Pure-SVG map of the realms plotted from latitude and longitude: bubbles sized by gold traded, coloured "
            "by threat band, dashed links within each region, graticule and compass. ImageUrl measure; Image visual.",
            [
     'VAR _R0 =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimRealm ), DimRealm[Realm], DimRealm[Region], DimRealm[ThreatBand], DimRealm[Latitude], DimRealm[Longitude] ),',
     '        "@g", [Total GoldVolume],',
     '        "@k", VAR _nm = DimRealm[Realm] RETURN CALCULATE ( [Total MonstersSlain], DimMonster[Habitat] = _nm )',
     '    )',
     'VAR _lo0 = MINX ( _R0, DimRealm[Longitude] )',
     'VAR _lo1 = MAXX ( _R0, DimRealm[Longitude] )',
     'VAR _la0 = MINX ( _R0, DimRealm[Latitude] )',
     'VAR _la1 = MAXX ( _R0, DimRealm[Latitude] )',
     'VAR _gMax = MAXX ( _R0, [@g] )',
     'VAR _R =',
     '    ADDCOLUMNS (',
     '        _R0,',
     f'        "@x", {L} + DIVIDE ( DimRealm[Longitude] - _lo0, _lo1 - _lo0 ) * {pw},',
     f'        "@y", {TOP} + DIVIDE ( _la1 - DimRealm[Latitude], _la1 - _la0 ) * {ph},',
     '        "@r", 8 + 22 * SQRT ( DIVIDE ( [@g], _gMax ) )',
     '    )',
     'VAR _GridV =',
     '    CONCATENATEX (',
     '        GENERATESERIES ( ROUNDUP ( _lo0 / 10, 0 ) * 10, _lo1, 10 ),',
     f'        VAR _x = FORMAT ( {L} + DIVIDE ( [Value] - _lo0, _lo1 - _lo0 ) * {pw}, "0" )',
     f"        RETURN \"<line x1='\" & _x & \"' y1='40' x2='\" & _x & \"' y2='{rh - 40}' stroke='#1c2840' stroke-width='1'/>\",",
     '        ""',
     '    )',
     'VAR _GridH =',
     '    CONCATENATEX (',
     '        GENERATESERIES ( ROUNDUP ( _la0 / 5, 0 ) * 5, _la1, 5 ),',
     f'        VAR _y = FORMAT ( {TOP} + DIVIDE ( _la1 - [Value], _la1 - _la0 ) * {ph}, "0" )',
     f"        RETURN \"<line x1='40' y1='\" & _y & \"' x2='{rw - 40}' y2='\" & _y & \"' stroke='#1c2840' stroke-width='1'/>\",",
     '        ""',
     '    )',
     'VAR _Links =',
     '    CONCATENATEX (',
     '        SUMMARIZE ( _R, DimRealm[Region] ),',
     '        VAR _reg = DimRealm[Region]',
     '        VAR _pts = FILTER ( _R, DimRealm[Region] = _reg )',
     '        VAR _a = TOPN ( 1, _pts, [@x], ASC )',
     '        VAR _b = TOPN ( 1, _pts, [@x], DESC )',
     '        VAR _x1 = MINX ( _a, [@x] ) VAR _y1 = MINX ( _a, [@y] )',
     '        VAR _x2 = MINX ( _b, [@x] ) VAR _y2 = MINX ( _b, [@y] )',
     '        RETURN',
     "            \"<line x1='\" & FORMAT ( _x1, \"0\" ) & \"' y1='\" & FORMAT ( _y1, \"0\" ) & \"' x2='\" & FORMAT ( _x2, \"0\" ) & \"' y2='\" & FORMAT ( _y2, \"0\" ) & \"' stroke='#c9a227' stroke-opacity='0.45' stroke-width='2' stroke-dasharray='6 7'/>\" &",
     "            \"<text x='\" & FORMAT ( ( _x1 + _x2 ) / 2, \"0\" ) & \"' y='\" & FORMAT ( MAX ( MIN ( _y1, _y2 ) - MAXX ( _pts, [@r] ) - 14, 96 ), \"0\" ) & \"' text-anchor='middle' font-family='Georgia,serif' font-size='13' letter-spacing='3' fill='#b8952a' stroke='#090e19' stroke-width='4' stroke-linejoin='round' paint-order='stroke'>\" & UPPER ( _reg ) & \"</text>\",",
     '        ""',
     '    )',
     'VAR _Marks =',
     '    CONCATENATEX (',
     '        _R,',
     f'        VAR _c = {_switch("DimRealm[ThreatBand]", THREAT_COLOUR, "#8aa0c0")}',
     '        VAR _cx = FORMAT ( [@x], "0" ) VAR _cy = FORMAT ( [@y], "0" )',
     '        RETURN',
     "            \"<circle cx='\" & _cx & \"' cy='\" & _cy & \"' r='\" & FORMAT ( [@r], \"0\" ) & \"' fill='\" & _c & \"' fill-opacity='0.2' stroke='\" & _c & \"' stroke-width='2'/>\" &",
     "            \"<circle cx='\" & _cx & \"' cy='\" & _cy & \"' r='4' fill='\" & _c & \"'/>\" &",
     "            \"<text x='\" & _cx & \"' y='\" & FORMAT ( [@y] + [@r] + 18, \"0\" ) & \"' text-anchor='middle' font-family='Georgia,serif' font-size='17' font-weight='700' fill='#f0cf5e' stroke='#090e19' stroke-width='4' stroke-linejoin='round' paint-order='stroke'>\" & DimRealm[Realm] & \"</text>\" &",
     f"            \"<text x='\" & _cx & \"' y='\" & FORMAT ( [@y] + [@r] + 34, \"0\" ) & \"' text-anchor='middle' font-family='Segoe UI,Arial,sans-serif' font-size='12' fill='#9fb3d1' stroke='#090e19' stroke-width='4' stroke-linejoin='round' paint-order='stroke'>\" & {_compact('[@g]')} & \" gold &#183; \" & {_compact('[@k]')} & \" slain</text>\",",
     '        ""',
     '    )',
     'RETURN',
     '    "data:image/svg+xml;utf8," &',
     f"    \"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {rw} {rh}'>\" &",
     f"    \"<defs><radialGradient id='sea' cx='0.5' cy='0.45' r='0.75'><stop offset='0' stop-color='#15203a'/><stop offset='1' stop-color='#090e19'/></radialGradient></defs>\" &",
     f"    \"<rect x='1' y='1' width='{rw - 2}' height='{rh - 2}' rx='16' fill='url(#sea)' stroke='#2a3953' stroke-width='2'/>\" &",
     '    _GridV & _GridH & _Links & _Marks &',
     f"    \"<text x='36' y='52' font-family='Georgia,serif' font-size='28' font-weight='700' letter-spacing='3' fill='#e8c349'>THE KNOWN REALMS</text>\" &",
     f"    \"<g transform='translate({rw - 70},72)'><circle r='30' fill='none' stroke='#2a3953' stroke-width='1.5'/><path d='M0 -38 L7 0 L0 38 L-7 0 Z' fill='#c9a227' fill-opacity='0.85'/><path d='M-38 0 L0 7 L38 0 L0 -7 Z' fill='#56688a'/><text y='-44' text-anchor='middle' font-family='Georgia,serif' font-size='14' fill='#c9a227'>N</text></g>\" &",
     f"    \"<g font-family='Segoe UI,Arial,sans-serif' font-size='13' fill='#8aa0c0'><circle cx='44' cy='{rh - 40}' r='6' fill='#f2c037'/><text x='56' y='{rh - 35}'>Medium</text><circle cx='134' cy='{rh - 40}' r='6' fill='#f97316'/><text x='146' y='{rh - 35}'>High</text><circle cx='208' cy='{rh - 40}' r='6' fill='#ff5a5a'/><text x='220' y='{rh - 35}'>Extreme threat &#183; bubble = gold traded</text></g>\" &",
     '    "</svg>"',
            ])


def realm_ledger(w, h):
    rw = 560
    rh = round(rw * h / w)
    return ("Realms Ledger HTML",
            "HTML-in-SVG ledger of the eight realms ordered by gold traded: region, terrain, threat band, a "
            "relative bar, gold traded and monsters slain in that habitat. ImageUrl measure; Image visual.",
            [
     'VAR _R =',
     '    ADDCOLUMNS (',
     '        SUMMARIZE ( ALLSELECTED ( DimRealm ), DimRealm[Realm], DimRealm[Region], DimRealm[Terrain], DimRealm[ThreatBand] ),',
     '        "@g", [Total GoldVolume],',
     '        "@k", VAR _nm = DimRealm[Realm] RETURN CALCULATE ( [Total MonstersSlain], DimMonster[Habitat] = _nm )',
     '    )',
     'VAR _Max = MAXX ( _R, [@g] )',
     'VAR _Rows =',
     '    CONCATENATEX (',
     '        _R,',
     f'        VAR _c = {_switch("DimRealm[ThreatBand]", THREAT_COLOUR, "#8aa0c0")}',
     '        VAR _pct = INT ( DIVIDE ( [@g], _Max ) * 100 )',
     '        RETURN',
     "            \"<div class='r'><div class='rh'><span class='nm'>\" & DimRealm[Realm] & \"</span><span class='th' style='color:\" & _c & \";border-color:\" & _c & \"'>\" & DimRealm[ThreatBand] & \"</span></div>\" &",
     "            \"<div class='mt'>\" & DimRealm[Region] & \" &#183; \" & DimRealm[Terrain] & \"</div>\" &",
     "            \"<div class='bb'><span style='width:\" & _pct & \"%'></span></div>\" &",
     f"            \"<div class='fm'>\" & {_compact('[@g]')} & \" gold traded &#183; \" & {_compact('[@k]')} & \" slain here</div></div>\",",
     '        "",',
     '        [@g], DESC',
     '    )',
     'RETURN',
     *_svg_open(w, h, rw, rh),
     "    \"<div xmlns='http://www.w3.org/1999/xhtml' class='rl'>\" &",
     '    "<style>" &',
     f'    ".rl{{width:{rw}px;height:{rh}px;box-sizing:border-box;display:flex;flex-direction:column;border-radius:16px;border:1px solid #2a3953;background:linear-gradient(180deg,#141d2f,#0c1220);padding:24px 30px 22px;font-family:Segoe UI,Arial,sans-serif;color:#e8edf5}}" &',
     '    ".rl .hd{font-family:Georgia,Cambria,serif;font-size:30px;font-weight:700;letter-spacing:3px;color:#e8c349;border-bottom:1px solid #2c3a52;padding-bottom:12px;margin-bottom:4px}" &',
     '    ".rl .r{flex:1;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #1b243a}.rl .r:last-child{border-bottom:none}" &',
     '    ".rl .rh{display:flex;align-items:center;justify-content:space-between}" &',
     '    ".rl .nm{font-family:Georgia,Cambria,serif;font-size:22px;font-weight:700;color:#f0cf5e}" &',
     '    ".rl .th{font-size:12px;letter-spacing:2px;text-transform:uppercase;border:1px solid;border-radius:999px;padding:2px 10px}" &',
     '    ".rl .mt{font-size:15px;color:#8aa0c0;margin-top:2px}" &',
     '    ".rl .bb{height:7px;background:#1f2a3d;border-radius:4px;overflow:hidden;margin-top:6px}.rl .bb span{display:block;height:100%;background:linear-gradient(90deg,#2f7a52,#6fd49b)}" &',
     '    ".rl .fm{font-size:15px;color:#b9c6da;margin-top:5px;font-variant-numeric:tabular-nums}" &',
     '    "</style>" &',
     "    \"<div class='hd'>REALM LEDGER</div>\" &",
     '    _Rows &',
     '    "</div></foreignObject></svg>"',
            ])


def quests_group(regions):
    return ("Quests", [fn(r["width"], r["height"]) for fn, r in
                       zip((quests_header, quest_chains, quest_danger, quest_rank), regions)])


def exchange_group(regions):
    return ("Exchange", [fn(r["width"], r["height"]) for fn, r in
                         zip((exchange_header, market_board, exchange_category, exchange_rarity), regions)])


def realms_group(regions):
    return ("Realms", [fn(r["width"], r["height"]) for fn, r in
                       zip((realms_header, realm_map, realm_ledger), regions)])


# ---- write -------------------------------------------------------------------------------------

def write_measures(tmdl_path, groups):
    """groups: [(displayFolder, [(name, description, body_lines), ...]), ...] -> the whole _HTML table.
    Refuses to write if a // comment would break Desktop or a measure nears the 32 KB string ceiling."""
    tags = _existing_tags(tmdl_path)
    lines = ["/// HTML-in-SVG presentation measures (foreignObject). Their own table on purpose: the synthetic-data",
             "/// hand-off rewrites _Measures.tmdl on every run, which would delete anything added there.",
             "table _HTML",
             T + "lineageTag: " + _tag(tags, "_HTML"),
             ""]
    written = []
    for folder, measures in groups:
        for name, desc, body in measures:
            if len("".join(body).encode("utf-8")) > 30000:
                raise SystemExit("refusing to write: %s is near the 32 KB measure-string ceiling" % name)
            lines.append(T + "/// " + desc)
            lines.append(T + f"measure '{name}' =")
            lines += [T * 3 + b for b in body]
            lines.append(T * 2 + "displayFolder: " + folder)
            lines.append(T * 2 + "lineageTag: " + _tag(tags, name))
            lines.append(T * 2 + "dataCategory: ImageUrl")
            lines.append("")
            written.append((folder, name))
    lines += [T + "column _",
              T * 2 + "lineageTag: " + _tag(tags, "_"),
              T * 2 + "isNameInferred",
              T * 2 + "sourceColumn: [_]",
              "",
              T + "partition _HTML = calculated",
              T * 2 + "mode: import",
              T * 2 + 'source = ROW ( "_", "" )',
              ""]
    text = CRLF.join(lines)
    if [l for l in text.splitlines() if l.strip().startswith("//") and not l.strip().startswith("///")]:
        raise SystemExit("refusing to write: // comment lines would break Desktop")
    with io.open(tmdl_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return written


def intro_group(regions):
    return ("Intro", [fn(r["width"], r["height"]) for fn, r in zip((hero, ledgers, legends, bosses), regions)])


def bestiary_group(regions):
    return ("Bestiary", [fn(r["width"], r["height"]) for fn, r in
                         zip((bestiary_header, bestiary_creatures, bestiary_families), regions)])
