# -*- coding: utf-8 -*-
"""Thème visuel STYLEMIND — CSS injecté + helpers d'affichage."""
import streamlit as st

# Palette
CREAM = "#FAF6F2"
INK = "#1A1523"
ACCENT = "#B34168"
ACCENT_SOFT = "#E7B5C7"
VIOLET = "#5B4B8A"
SAUGE = "#9CAF88"
GOLD = "#C9A227"

CSS = """
<style>
/* ── Global ─────────────────────────────────────────────── */
html, body, .stApp{
  background: #FAF6F2;
  color: #1A1523;
}
section.main > div {padding-top: 1.2rem;}
h1, h2, h3 {font-weight: 700; letter-spacing: -0.01em;}

/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #1A1523 0%, #2A1F33 100%);
}
[data-testid="stSidebar"] *{ color: #F5EBDD !important; }
[data-testid="stSidebar"] .stButton > button{
  width: 100%; text-align: left; background: transparent;
  color: #F5EBDD !important; border: 1px solid rgba(245,235,221,.18);
  border-radius: 12px; margin-bottom: 6px; transition: all .2s;
}
[data-testid="stSidebar"] .stButton > button:hover{
  background: rgba(212,130,158,.22); border-color: #D4829E;
  transform: translateX(3px);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]{
  background: linear-gradient(90deg,#B34168,#5B4B8A); border: none;
}

/* ── Hero & titres ───────────────────────────────────────── */
.hero{
  background: linear-gradient(120deg, #1A1523 0%, #4A2E52 45%, #B34168 100%);
  border-radius: 24px; padding: 34px 38px; color: #F5EBDD; margin-bottom: 22px;
}
.hero h1{ font-size: 2rem; margin: 0 0 8px 0; color: #fff !important;}
.hero p{ margin: 0; opacity: .88; font-size: 1rem; max-width: 720px;}
.hero .chiprow{ margin-top: 14px;}

/* ── Chips / badges ──────────────────────────────────────── */
.chip{
  display: inline-block; padding: 3px 11px; border-radius: 999px;
  font-size: .72rem; font-weight: 600; margin: 0 6px 6px 0;
  background: rgba(212,130,158,.14); color: #7C2D3A;
  border: 1px solid rgba(179,65,104,.25);
  max-width: 100%; overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; vertical-align: middle;
}
.demo-chip{
  display: inline-block; padding: 2px 8px; border-radius: 999px;
  font-size: .68rem; font-weight: 700; background: #FFF3C9;
  color: #8A6D1D; border: 1px dashed #C9A227; margin: 0 6px 6px 0;
}
.chip-sponsored{ background: #EADAF7; color: #5B4B8A; border-color: #5B4B8A55;}
.chip-eco{ background: #E4EFDD; color: #4A6741; border-color: #4A674155;}
.chip-second{ background: #FDE8DC; color: #A0522D; border-color: #A0522D55;}
.chip-follow{ background: #E8E4F7; color: #5B4B8A; border-color: #5B4B8A55;}
.chip-premium{ background: linear-gradient(90deg,#C9A227,#B34168); color:#fff; border:none;}

/* ── Tuiles visuelles ────────────────────────────────────── */
.tile{
  border-radius: 18px; color:#fff; position: relative; overflow: hidden;
  box-shadow: 0 8px 24px rgba(26,21,35,.10); margin-bottom: 2px;
  display:flex; align-items:flex-end;
}
.tile .tile-img{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; display:block;
}
.tile .overlay{
  position:relative; z-index:2;
  width:100%; padding: 30px 14px 12px 14px;
  background: linear-gradient(180deg, transparent 0%, rgba(26,21,35,.62) 130%);
  box-sizing: border-box;
}
.tile .t-title{ font-weight: 700; font-size: .95rem; line-height: 1.25;
  text-shadow: 0 1px 6px rgba(0,0,0,.5);}
.tile .t-sub{ font-size: .75rem; opacity: .9; margin-top: 2px;}
.tile .t-price{ font-size: .8rem; opacity: .95; font-weight: 700; margin-top: 4px;}
.tile .t-badge{
  position: absolute; top: 10px; left: 10px; padding: 3px 9px; z-index:2;
  border-radius: 999px; font-size: .68rem; font-weight: 700;
  background: rgba(255,255,255,.9); color: #1A1523;
}
.tile .t-badge.badge-sponsored{ background:#5B4B8A; color:#fff;}
.tile .t-badge.badge-demo{ background:#FFF3C9; color:#8A6D1D; border:1px dashed #C9A227;}
.tile .swatches{ position: absolute; top: 12px; right: 12px; display:flex; gap:4px; z-index:2;}
.sw{ width:14px; height:14px; border-radius:50%; border:1.5px solid rgba(255,255,255,.85);}

/* ── Cartes profil / stats ───────────────────────────────── */
.stat-card{
  background:#fff; border-radius:18px; padding:18px 20px; margin-bottom:12px;
  box-shadow: 0 4px 16px rgba(26,21,35,.06); border: 1px solid #F0E6DC;
}
.stat-card .v{ font-size: clamp(1.05rem, 2.6vw, 1.5rem); font-weight: 800;
  color:#B34168; overflow-wrap: anywhere;}
.stat-card .k{ font-size: .78rem; color:#7A7284; text-transform: uppercase;
  letter-spacing:.06em;}
.bar{ height:8px; border-radius:6px; background:#F0E6DC; overflow:hidden; margin: 4px 0 10px 0;}
.bar > div{ height:100%; background: linear-gradient(90deg,#B34168,#5B4B8A); border-radius:6px;}

/* ── Cartes tenues IA ────────────────────────────────────── */
.outfit-card{
  background:#fff; border-radius:20px; padding:18px; margin-bottom:14px;
  box-shadow: 0 4px 18px rgba(26,21,35,.07); border:1px solid #F0E6DC;
}
.outfit-card h4{ margin: 0 0 4px 0;}
.why{ font-size: .8rem; color:#5D5468; background:#FAF3ED; border-left: 3px solid #B34168;
  padding: 8px 12px; border-radius: 0 10px 10px 0; margin-top: 8px;}

/* ── Chat ────────────────────────────────────────────────── */
[data-testid="stChatInput"] > div{ border-radius: 14px;}
.chip-quick{ margin: 4px 6px 4px 0;}

/* ── Boutons ─────────────────────────────────────────────── */
.stButton > button{
  border-radius: 12px; font-size: .85rem; transition: all .18s;
  min-height: 2.4rem;
}
.stButton > button:hover{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(179,65,104,.18);}
.stButton > button:focus-visible{ outline: 2px solid #B34168; outline-offset: 2px;}
.stButton > button:disabled{ opacity: .45; transform: none; box-shadow: none;}
.tile{ transition: transform .18s, box-shadow .18s;}
.tile:hover{ transform: translateY(-2px); box-shadow: 0 12px 28px rgba(26,21,35,.14);}

/* ── Responsive : mobile ─────────────────────────────────── */
@media (max-width: 640px){
  .hero{ padding: 22px 20px; border-radius: 18px;}
  .hero h1{ font-size: 1.5rem;}
  .stat-card{ padding: 14px 16px;}
  .outfit-card{ padding: 14px;}
}

.divider-soft{ height:1px; background:#EFE3D8; margin: 18px 0;}
"""


def inject():
    """Injecte le CSS global une fois par exécution."""
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def chips(labels, cls="chip"):
    """Série de chips HTML."""
    return "".join(f'<span class="{cls}">{l}</span>' for l in labels)


def demo_chip() -> str:
    """Badge « Données de démo » — obligatoire partout où le contenu
    est simulé en attendant les vraies intégrations (API, catalogue)."""
    return '<span class="demo-chip">DÉMO</span>'


def hero(title: str, text: str, chips_html: str = ""):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{text}</p>'
        f'<div class="chiprow">{chips_html}</div></div>',
        unsafe_allow_html=True,
    )


def stat_card(value: str, label: str):
    """Petite carte chiffre-clé (HTML pur)."""
    st.markdown(
        f'<div class="stat-card"><div class="v">{value}</div>'
        f'<div class="k">{label}</div></div>',
        unsafe_allow_html=True,
    )


def style_bar(name: str, pct: float):
    """Mini barre de progression HTML (0-100)."""
    pct = max(0, min(100, int(pct)))
    st.markdown(
        f'<div style="font-size:.8rem">{name}</div>'
        f'<div class="bar"><div style="width:{pct}%"></div></div>',
        unsafe_allow_html=True,
    )
