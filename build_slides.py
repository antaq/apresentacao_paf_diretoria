#!/usr/bin/env python3
"""Gera os slides 02..16 da apresentação PAF 2027 — Apresentação ao Diretor-Geral.

Mesmo esqueleto do deck IPR 2.0 do Encontro de Chefias
(EncontroChefias2026/apresentacao_ipr_paf2027/build_slides.py): barra azul +
barra clara no topo, cabeçalho com kicker e título, corpo livre e rodapé com o
número do slide. A capa (01) e o encerramento (17) são escritos à mão.

Dois blocos de conteúdo:
  Bloco 1 (03..07) — fiscalizações do grupo de risco (IPR 2.0), textos do
                     deck do Encontro de Chefias e do painel IPR-PAF.
  Bloco 2 (08..15) — fiscalizações temáticas, a partir da Nota Técnica
                     nº 27/2026/GPF/SFC (SEI 3024667) e da apresentação ao DG.

Para regerar: python3 build_slides.py
"""

from pathlib import Path

DST = Path(__file__).resolve().parent
TOTAL = 19
RODAPE = "PAF 2027 — Apresentação ao Diretor-Geral · SFC · GRAT, GPF e GCOR · ANTAQ"
# Fator global de texto. Cada slide declara o `base` em que foi fechado; este
# fator multiplica todos eles de uma vez. Em 0.90 o texto do corpo encolhe 10%,
# e a folga que sobra vira respiro vertical entre os cards (row-gap, abaixo).
TEXT_SCALE = 0.90

BASE_CSS = """
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background:#ffffff; }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.text-brand { color:#003366; }
.bg-brand { background-color:#003366; }
.text-accent { color:#0066CC; }
.bg-accent { background-color:#0066CC; }
.header-bar { height:10px; background:#003366; width:100%; }
.secondary-bar { height:4px; background:#0066CC; width:100%; }

.stat-card {
  background: linear-gradient(135deg, #003366, #004d99);
  border-radius: 16px;
  padding: 20px 18px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
}
.stat-card::after {
  content: '';
  position: absolute; top: -30px; right: -30px;
  width: 80px; height: 80px;
  border-radius: 50%;
  background: rgba(255,255,255,0.06);
}
.stat-num {
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;
  font-size: calc(48px * var(--tz));
  line-height: 1;
}
.card {
  display: flex; align-items: flex-start; gap: 16px;
  padding: 14px 20px;
  background: #F8FAFC;
  border-radius: 14px;
  border-left: 5px solid #0066CC;
}
.card-green  { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-left-color:#22C55E; }
.card-amber  { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#F59E0B; }
.card-red    { background: linear-gradient(135deg,#FEF2F2,#FEE2E2); border-left-color:#EF4444; }
.ico {
  width:50px; height:50px; border-radius:12px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
}
/* As colunas dos slides de duas metades centram o proprio conteudo: a folga
   vertical fica dividida em cima e embaixo, em vez de sobrar toda no rodape.
   O contêiner de conteudo quase sempre E o proprio grid (`class="flex-1 ...
   grid"`), e nao um grid dentro dele — por isso os dois seletores. */
.slide > .flex-1 > .flex.flex-col,
.slide > .flex-1 > .grid > .flex.flex-col { justify-content:center; }

table.tbl { width:100%; border-collapse:collapse; }
table.tbl th {
  background:#F1F5F9; color:#475569; text-align:left;
  font-family:'Montserrat',sans-serif; font-weight:700;
  text-transform:uppercase; letter-spacing:0.06em;
  padding:10px 14px; font-size:calc(15px * var(--tz));
}
table.tbl td { padding:11px 14px; border-top:1px solid #E2E8F0; color:#334155; font-size:calc(18px * var(--tz)); }
table.tbl tr:nth-child(even) td { background:#FAFBFC; }
.num { text-align:right; font-variant-numeric:tabular-nums; }
table.tbl th.num { text-align:right; }
.pill {
  display:inline-block; padding:3px 12px; border-radius:999px;
  font-family:'Montserrat',sans-serif; font-weight:700;
  font-size:calc(14px * var(--tz)); letter-spacing:0.04em;
}
.pill-a { background:#DCFCE7; color:#166534; }
.pill-b { background:#DBEAFE; color:#1E40AF; }
.pill-c { background:#FEE2E2; color:#991B1B; }
.pill-gold { background:#FEF3C7; color:#92400E; }
.formula {
  background:#0F172A; color:#E2E8F0; border-radius:14px;
  padding:18px 24px; font-family:'Courier New',monospace;
  font-size:calc(20px * var(--tz)); letter-spacing:0.02em;
}
.destaque {
  background: linear-gradient(135deg,#003366,#0066CC);
  color:#fff; border-radius:16px; padding:16px 24px;
}
.legenda { color:#64748B; font-size:calc(15px * var(--tz)); line-height:1.5; }
.novo-tag {
  display:inline-flex; align-items:center; gap:7px;
  background:#FFD700; color:#003366; border-radius:999px;
  padding:3px 14px; font-family:'Montserrat',sans-serif;
  font-weight:900; font-size:calc(13px * var(--tz));
  letter-spacing:0.1em; text-transform:uppercase;
}

/* Respiro vertical entre os cards.
   Os utilitarios gap-* do Tailwind valem para as duas direcoes, e mexer no
   `gap` cheio estreitaria as colunas dos grids de duas metades. Por isso aqui
   so o `row-gap` e reescrito: um card fica mais longe do card de baixo, e a
   largura das colunas continua exatamente a mesma. Esta folha vem depois do
   CDN no <head>, entao vence no desempate por ordem. */
.gap-2 { row-gap:18px; }
.gap-3 { row-gap:30px; }
.gap-4 { row-gap:32px; }
.gap-5 { row-gap:34px; }
.gap-6 { row-gap:34px; }
.gap-8 { row-gap:38px; }
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>{css}</style>
</head>
<body>
<div class="slide">
  <div class="header-bar"></div>
  <div class="secondary-bar"></div>

  <div class="px-16 pt-6 pb-2">
    <div class="flex items-center gap-3">
      <div style="width:5px;height:44px;" class="bg-accent"></div>
      <div>
        <p class="font-montserrat font-bold text-gray-400 text-lg uppercase tracking-widest">{kicker}</p>
        <p class="text-5xl font-montserrat font-bold text-brand uppercase tracking-tight">{titulo}</p>
      </div>
      <div class="ml-auto flex items-center gap-3">
        {tag}
        <img src="assets/logo-antaq-azul.png" alt="ANTAQ" style="height:32px;">
        <p class="font-montserrat font-bold text-gray-400 tracking-wider" style="font-size:12px; line-height:1.35;">SFC<br/>GRAT · GPF · GCOR</p>
      </div>
    </div>
  </div>

{body}

  <div class="px-16 pb-4 flex justify-between items-center border-t border-gray-100 pt-3 mx-8">
    <p class="text-gray-400 text-sm">{rodape}</p>
    <p class="text-gray-300 text-sm font-mono">{n} / {total}</p>
  </div>
</div>
<script src="zoom.js"></script>
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""

TAG_NOVO = '<span class="novo-tag"><i class="fas fa-star"></i> Novidade 2027</span>'

SLIDES: list[dict] = []
def slide(n, title, kicker, titulo, body, extra_css="", tag="", base=1.0):
    SLIDES.append(
        dict(n=n, title=title, kicker=kicker, titulo=titulo, body=body,
             extra_css=extra_css, tag=tag, base=base)
    )



# Acréscimos deste deck ao CSS comum: etiqueta de bloco, fonte, gráficos de barra.
BASE_CSS += """
.bloco-tag {
  display:inline-flex; align-items:center; gap:8px;
  border-radius:999px; padding:4px 16px; font-family:'Montserrat',sans-serif;
  font-weight:900; font-size:calc(13px * var(--tz)); letter-spacing:0.08em; text-transform:uppercase;
}
.bt-risco { background:#FEE2E2; color:#991B1B; }
.bt-tema  { background:#DBEAFE; color:#1E3A8A; }
.bt-geral { background:#FEF3C7; color:#92400E; }
.fonte { color:#94A3B8; font-size:calc(13px * var(--tz)); line-height:1.4; }
.titulo-sec { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(21px * var(--tz)); }
.sub-sec { color:#64748B; font-size:calc(15px * var(--tz)); }
.num-badge {
  width:38px; height:38px; border-radius:50%; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  background:#003366; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900;
  font-size:calc(17px * var(--tz));
}
.card p { margin:0; }
.card-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(19px * var(--tz)); }
.card-d { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.45; margin-top:3px !important; }

/* Barras: trilho cinza, segmentos com 2px de folga entre si e rótulo direto. */
.bar-row { display:grid; grid-template-columns: var(--rot, 300px) 1fr; align-items:center; gap:14px; }
.bar-rot { color:#334155; font-size:calc(17px * var(--tz)); line-height:1.25; text-align:right; }
.bar-rot strong { color:#003366; }
.bar-trk { display:flex; gap:2px; height:42px; }
.seg {
  height:100%; display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(17px * var(--tz));
  color:#fff; min-width:0; overflow:hidden; white-space:nowrap;
}
.seg:first-child { border-radius:4px 0 0 4px; }
.seg:last-child  { border-radius:0 4px 4px 0; }
.seg:only-child  { border-radius:4px; }
.leg-row { display:flex; flex-wrap:wrap; gap:22px; color:#475569; font-size:calc(16px * var(--tz)); }
.leg-row span { display:inline-flex; align-items:center; gap:7px; }
.leg-row i.sw { width:18px; height:18px; border-radius:3px; display:inline-block; }
/* Título com tamanho fixo em todos os slides: não acompanha o fator de texto,
   para que títulos longos não quebrem linha quando o corpo cresce. */
.slide p.text-5xl { font-size:54px !important; line-height:1.1 !important; }
"""

TAG_GERAL = '<span class="bloco-tag bt-geral"><i class="fas fa-compass"></i> Visão geral</span>'
TAG_RISCO = '<span class="bloco-tag bt-risco"><i class="fas fa-gauge-high"></i> Bloco 1 · Grupo de risco</span>'
TAG_TEMA = '<span class="bloco-tag bt-tema"><i class="fas fa-layer-group"></i> Bloco 2 · Temáticas</span>'
NT = "NT nº 27/2026/GPF/SFC"

# Escala de alcance: ordinal, então rampa sequencial de um azul só (mais escuro =
# mais alcance) e cinza neutro para "sem aderência". Rótulo direto em todo segmento.
C_INT, C_PAR, C_IND, C_SEM = "#003366", "#2F6FB3", "#8DB8E6", "#CBD5E1"
# Situação das matérias: categorias de estado, cada uma com rótulo e legenda.
C_ATD, C_CNV, C_NOV, C_ART, C_FORA = "#15803D", "#0066CC", "#D97706", "#7C3AED", "#64748B"


def barra(rotulo, segs, total, titulo=""):
    """Uma linha de barra empilhada. segs = [(valor, cor, cor_texto), ...]."""
    partes = []
    for v, cor, txt in segs:
        if not v:
            continue
        partes.append(
            f'<div class="seg" style="width:{100 * v / total:.2f}%;background:{cor};color:{txt};" '
            f'title="{titulo}{v}">{v}</div>'
        )
    return (f'<div class="bar-row"><div class="bar-rot">{rotulo}</div>'
            f'<div class="bar-trk">{"".join(partes)}</div></div>')


# ===========================================================================
# BLOCO 2 — FISCALIZAÇÕES TEMÁTICAS (NT 27/2026)
# ===========================================================================

# ---------------------------------------------------------------------------
# 08 — Contexto e premissa
# ---------------------------------------------------------------------------
slide(
    8,
    "Temáticas — contexto e premissa",
    f"Fiscalizações temáticas · {NT}",
    "Por que e com que acervo",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">Origem da demanda</p>
      <div class="card">
        <div class="num-badge">1</div>
        <div>
          <p class="card-t">Deliberação-DG nº 96/2025</p>
          <p class="card-d">Referendada pelo Acórdão nº 41-2026-ANTAQ: discutir previamente a proposta
          do PAF com as unidades finalísticas e as Diretorias, para captar temáticas ainda não mapeadas.</p>
        </div>
      </div>
      <div class="card">
        <div class="num-badge">2</div>
        <div>
          <p class="card-t">Ofício Circular nº 2/2026/SFC/ANTAQ</p>
          <p class="card-d">Consulta à SRG, à SESGI, à SOG e à SEPH sobre fiscalizações temáticas
          relevantes, com prazo encerrado em <strong>17/08/2026</strong>.</p>
        </div>
      </div>
      <div class="card card-amber">
        <div class="num-badge" style="background:#B45309;">3</div>
        <div>
          <p class="card-t">O limite da consulta interna</p>
          <p class="card-d">As fontes da Agência registram o que já chegou a ela. O problema que
          <strong>não gera autuação nem manifestação</strong> fica invisível ao planejamento — daí a
          avaliação das contribuições externas.</p>
        </div>
      </div>
    </div>

    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">O acervo já existia: revisão da Agenda Regulatória 2025-2028</p>
      <div class="grid grid-cols-4 gap-3">
        <div class="stat-card"><p class="stat-num">99</p><p class="text-blue-200 text-sm font-semibold mt-2">contribuições validadas<br/>(17/04 a 05/06/2026)</p></div>
        <div class="stat-card"><p class="stat-num">90</p><p class="text-blue-200 text-sm font-semibold mt-2">do público externo,<br/>em 65 formulários</p></div>
        <div class="stat-card"><p class="stat-num">8</p><p class="text-blue-200 text-sm font-semibold mt-2">de unidades internas<br/>(3 da SFC)</p></div>
        <div class="stat-card"><p class="stat-num">1</p><p class="text-blue-200 text-sm font-semibold mt-2">do Poder Concedente<br/>(MPor)</p></div>
      </div>
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(21px * var(--tz));">Tomada de Subsídios dispensada neste ciclo</p>
        <p class="text-blue-100 text-lg mt-1">
          <strong>Mesmo universo de respondentes</strong> que uma consulta própria buscaria (Res. ANTAQ nº 40/2021, art. 2º);
          <strong>volume e aderência</strong> — 4 eixos, 25 subgrupos, gargalos concretos da operação;
          e o <strong>custo</strong> de repetir: fadiga de participação, sobreposição com o ciclo regulatório
          e prazo da DC em 31/10/2026. O acervo foi examinado <strong>na íntegra</strong>, sem recorte prévio.
        </p>
      </div>
      <div class="card card-green">
        <div class="ico" style="background:#BBF7D0;"><i class="fas fa-calendar-plus text-green-700 text-2xl"></i></div>
        <div>
          <p class="card-t">Para os próximos ciclos</p>
          <p class="card-d">Consulta externa no calendário regular do PAF, aberta no 1º semestre e articulada
          com a SRG, gestora da participação social no ciclo regulatório.</p>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Relatório Técnico nº 4/2026/CGGR/SRG · Processo nº 50300.009940/2026-03. Fonte: {NT}, itens 2 e 3.</p>
""",
    tag=TAG_TEMA,
    base=1.48,
)

# ---------------------------------------------------------------------------
# 09 — Metodologia e panorama
# ---------------------------------------------------------------------------
slide(
    9,
    "Temáticas — metodologia",
    f"Metodologia · {NT}, item 4",
    "Da demanda à Ordem de Serviço",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="grid grid-cols-4 gap-4">
      <div class="etapa">
        <div class="etapa-n">1</div>
        <p class="card-t">Agrupar</p>
        <p class="card-d">99 contribuições em <strong>25 subgrupos</strong> (árvore hierárquica), em 4 eixos:
        Instalações Portuárias e Terminais, Navegação Interior, Navegação Marítima e Transversal.</p>
      </div>
      <div class="etapa">
        <div class="etapa-n">2</div>
        <p class="card-t">Confrontar</p>
        <p class="card-d">Com três instrumentos: <strong>Agenda Regulatória</strong> (21 temas vigentes),
        <strong>Agenda Plurianual de Estudos</strong> (27 estudos) e as <strong>7 temáticas do PAF 2026</strong>
        (OS nº 3/2026/SFC).</p>
      </div>
      <div class="etapa">
        <div class="etapa-n">3</div>
        <p class="card-t">Classificar o alcance</p>
        <p class="card-d">Cada bloco recebe um grau de alcance frente a cada instrumento, na escala abaixo.</p>
      </div>
      <div class="etapa" style="border-color:#0066CC; background:#EFF6FF;">
        <div class="etapa-n" style="background:#0066CC;">4</div>
        <p class="card-t">Confronto fino</p>
        <p class="card-d"><strong>63 contribuições</strong> frente aos itens efetivamente cobrados nas Ordens de
        Serviço em curso: <strong>33 matérias</strong>. Somam-se 10 matérias das Superintendências finalísticas.</p>
      </div>
    </div>

    <div class="grid grid-cols-4 gap-3">
      <div class="esc" style="border-left-color:{C_INT};"><span class="esc-t">Integral</span><span class="esc-d">abrange todo o bloco, sem demanda residual</span></div>
      <div class="esc" style="border-left-color:{C_PAR};"><span class="esc-t">Parcial</span><span class="esc-d">há sobreposição, mas parte do bloco fica fora</span></div>
      <div class="esc" style="border-left-color:{C_IND};"><span class="esc-t">Indireta</span><span class="esc-d">vínculo por finalidade, não por objeto</span></div>
      <div class="esc" style="border-left-color:{C_SEM};"><span class="esc-t">Sem aderência</span><span class="esc-d">nenhum tema, estudo ou fiscalização alcança</span></div>
    </div>

    <div class="flex-1 grid grid-cols-12 gap-6 items-center">
      <div class="col-span-4 grid grid-cols-2 gap-3">
        <div class="stat-card"><p class="stat-num">61</p><p class="text-blue-200 text-sm font-semibold mt-2">demandas no eixo<br/>portuário (14 blocos)</p></div>
        <div class="stat-card" style="background:linear-gradient(135deg,#475569,#64748B);"><p class="stat-num">4</p><p class="text-gray-200 text-sm font-semibold mt-2">na Navegação Interior,<br/>sobre a taxa de seca</p></div>
      </div>
      <div class="col-span-8 flex flex-col gap-3" style="--rot:380px;">
        <p class="titulo-sec">Três blocos respondem por 40 das 99 demandas</p>
        {barra("<strong>Afretamento, outorgas</strong> e regime de bandeira", [(18, C_INT, "#fff")], 18, "Demandas: ")}
        {barra("<strong>Preços, tarifas</strong> e abusividade nas cobranças", [(11, C_INT, "#fff")], 18, "Demandas: ")}
        {barra("<strong>Sobre-estadia</strong> de contêineres", [(11, C_INT, "#fff")], 18, "Demandas: ")}
        <p class="legenda">Demandas de movimentação e armazenagem de contêineres foram para o eixo portuário;
        continuidade da navegação em estiagem severa, para a Navegação Interior.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Planilhas de classificação AR, APE e fiscalizações temáticas: SEI nº 3024868. Fonte: {NT}, itens 4 e 5.1.</p>
""",
    extra_css="""
.etapa { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:16px 18px; position:relative; }
.etapa p { margin:0; }
.etapa-n {
  width:36px; height:36px; border-radius:10px; background:#003366; color:#fff;
  display:flex; align-items:center; justify-content:center; margin-bottom:10px;
  font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(17px * var(--tz));
}
.esc { border-left:8px solid; background:#F8FAFC; border-radius:10px; padding:9px 14px; display:flex; flex-direction:column; }
.esc-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(16px * var(--tz)); }
.esc-d { color:#64748B; font-size:calc(14px * var(--tz)); }
""",
    tag=TAG_TEMA,
    base=1.36,
)

# ---------------------------------------------------------------------------
# 10 — Confronto com os três instrumentos
# ---------------------------------------------------------------------------
_esc = lambda i, p, d, s: [(i, C_INT, "#fff"), (p, C_PAR, "#fff"), (d, C_IND, "#003366"), (s, C_SEM, "#334155")]
slide(
    10,
    "Temáticas — confronto com os instrumentos",
    f"Resultados · {NT}, itens 5.2 a 5.5",
    "Quem já alcança as 99 demandas",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-7 flex flex-col justify-center gap-5" style="--rot:250px;">
      <div>
        <p class="titulo-sec">Alcance de cada instrumento sobre as 99 demandas</p>
        <p class="sub-sec">número de demandas por grau de alcance</p>
      </div>
      <div class="leg-row">
        <span><i class="sw" style="background:{C_INT};"></i>Integral</span>
        <span><i class="sw" style="background:{C_PAR};"></i>Parcial</span>
        <span><i class="sw" style="background:{C_IND};"></i>Indireta</span>
        <span><i class="sw" style="background:{C_SEM};"></i>Sem aderência</span>
      </div>
      {barra("<strong>Agenda Regulatória</strong><br/>2025-2028", _esc(42, 27, 7, 23), 99)}
      {barra("<strong>Agenda de Estudos</strong><br/>2025/2028", _esc(28, 45, 7, 19), 99)}
      {barra("<strong>Fiscalizações temáticas</strong><br/>PAF 2026", _esc(43, 32, 0, 24), 99)}
      <div class="grid grid-cols-2 gap-4 mt-2">
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-book text-accent text-2xl"></i></div>
          <div><p class="card-t">Agenda Regulatória</p>
          <p class="card-d">Tema 2.6 é o principal de 5 blocos (31 demandas). Os temas 1.1 a 1.4, de
          Navegação Interior, não foram alcançados.</p></div>
        </div>
        <div class="card">
          <div class="ico" style="background:#DBEAFE;"><i class="fas fa-flask text-accent text-2xl"></i></div>
          <div><p class="card-t">Agenda de Estudos</p>
          <p class="card-d">24 dos 27 estudos alcançados; ficam sem demanda P11, P16 e P20
          (navegação interior e passageiros).</p></div>
        </div>
      </div>
    </div>

    <div class="col-span-5 flex flex-col justify-center gap-4">
      <div class="destaque flex items-center gap-5">
        <p class="font-montserrat font-black" style="font-size:calc(60px * var(--tz)); line-height:1;">70</p>
        <p class="text-blue-100 text-xl">demandas, em 11 blocos, são alcançadas <strong>pelos três instrumentos</strong> ao mesmo tempo</p>
      </div>
      <div class="descob">
        <div class="flex items-center gap-4 mb-3">
          <p class="font-montserrat font-black text-brand" style="font-size:calc(48px * var(--tz)); line-height:1;">14</p>
          <p class="card-t">demandas, em 6 blocos,<br/>sem cobertura em nenhum instrumento</p>
        </div>
        <ul>
          <li>Inovação e cibersegurança</li>
          <li>Avaliação de resultado regulatório</li>
          <li>Terminais de passageiros e biometria</li>
          <li>Resíduos de embarcações</li>
          <li>Modelo de fiscalização e supervisão regulatória</li>
          <li>Padronização e compartilhamento de dados marítimos</li>
        </ul>
        <p class="legenda mt-3">Esses blocos descobertos orientam o critério de <strong>complementaridade</strong> na escolha das novas temáticas.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {NT}, itens 5.2 a 5.5.</p>
""",
    extra_css="""
.descob { background:#FFFBEB; border:1px solid #FDE68A; border-radius:16px; padding:18px 22px; }
.descob p { margin:0; }
.descob ul { margin:0; padding:0; list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:8px 18px; }
.descob li { color:#334155; font-size:calc(16px * var(--tz)); padding-left:20px; position:relative; line-height:1.35; }
.descob li::before { content:''; position:absolute; left:2px; top:calc(8px * var(--tz)); width:9px; height:9px; border-radius:2px; background:#D97706; }
""",
    tag=TAG_TEMA,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 11 — Alcance das temáticas do PAF 2026 e as 33 matérias
# ---------------------------------------------------------------------------
_t26 = [
    ("Preço em terminais de contêineres", 6, 36),
    ("Contabilização de TPB no REB", 1, 18),
    ("Diagnóstico do desempenho das APs", 6, 17),
    ("Atraso e omissão de navios de contêineres", 1, 7),
    ("Estrutura de fiscalização das APs", 1, 4),
    ("Embarcações do transporte misto", 0, 0),
    ("Diagnóstico dos Convênios de Delegação", 0, 0),
]
_rows26 = "\n".join(
    barra(f"{n} <span style='color:#94A3B8;'>({b})</span>", [(d, C_INT, "#fff")], 36, "Demandas: ")
    if d else
    f'<div class="bar-row"><div class="bar-rot">{n} <span style="color:#94A3B8;">(0)</span></div>'
    f'<div class="text-gray-400 text-base italic">nenhuma demanda externa associada</div></div>'
    for n, b, d in _t26
)
slide(
    11,
    "Temáticas — o que as atuais já cobrem",
    f"Resultados · {NT}, itens 5.4 a 5.7",
    "O que as temáticas de 2026 já cobrem",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-8">
    <div class="col-span-7 flex flex-col justify-center gap-3" style="--rot:330px;">
      <div>
        <p class="titulo-sec">Demandas externas associadas a cada temática em execução</p>
        <p class="sub-sec">blocos entre parênteses</p>
      </div>
      {_rows26}
      <div class="card mt-1">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-magnifying-glass-chart text-accent text-2xl"></i></div>
        <div><p class="card-d" style="margin-top:0 !important;"><strong>Preço em contêineres</strong> é a de maior alcance. A temática de <strong>TPB</strong> alcança só
        em parte o maior bloco da consulta: apura a tonelagem para inscrição no REB, não afretamento e outorgas.</p></div>
      </div>
    </div>

    <div class="col-span-5 flex flex-col justify-center gap-3">
      <div>
        <p class="titulo-sec">33 matérias frente às Ordens de Serviço em curso</p>
        <p class="sub-sec">63 contribuições examinadas item a item</p>
      </div>
      <div class="sit" style="border-left-color:{C_ATD};"><span class="sit-n" style="color:{C_ATD};">11</span><span class="sit-d"><strong>atendidas</strong> no ciclo corrente</span></div>
      <div class="sit" style="border-left-color:{C_CNV};"><span class="sit-n" style="color:{C_CNV};">3</span><span class="sit-d"><strong>conversíveis</strong> na consolidação dos resultados já produzidos</span></div>
      <div class="sit" style="border-left-color:{C_NOV}; background:#FFFBEB;"><span class="sit-n" style="color:{C_NOV};">9</span><span class="sit-d">dependem de <strong>novo ciclo</strong> de fiscalização — 7 delas em contêineres</span></div>
      <div class="sit" style="border-left-color:{C_ART};"><span class="sit-n" style="color:{C_ART};">4</span><span class="sit-d">dependem de <strong>articulação</strong> com as áreas de afretamento e outorgas</span></div>
      <div class="sit" style="border-left-color:{C_FORA};"><span class="sit-n" style="color:{C_FORA};">6</span><span class="sit-d"><strong>sem método</strong> de aferição ou fora da verificação de conformidade</span></div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-scale-balanced text-yellow-700 text-2xl"></i></div>
        <div><p class="card-d" style="margin-top:0 !important;">É essa distribuição que sustenta <strong>manter quatro temáticas</strong> com escopo ajustado e <strong>substituir as três</strong> demais.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">APs: Autoridades Portuárias · REB: Registro Especial Brasileiro. Numeração das contribuições conforme o Relatório Técnico nº 4/2026/CGGR/SRG. Fonte: {NT}, Quadros 1 e 2.</p>
""",
    extra_css="""
.sit { display:flex; align-items:center; gap:18px; background:#F8FAFC; border-left:7px solid; border-radius:12px; padding:9px 18px; }
.sit-n { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(36px * var(--tz)); line-height:1; min-width:48px; text-align:center; }
.sit-d { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.35; }
.sit-d strong { color:#003366; }
""",
    tag=TAG_TEMA,
    base=1.46,
)

# ---------------------------------------------------------------------------
# 12 — Leitura por temática
# ---------------------------------------------------------------------------
def _mini(atd, cnv, nov, art, fora):
    tot = atd + cnv + nov + art + fora
    return barra("", [(atd, C_ATD, "#fff"), (cnv, C_CNV, "#fff"), (nov, C_NOV, "#fff"),
                      (art, C_ART, "#fff"), (fora, C_FORA, "#fff")], tot)

slide(
    12,
    "Temáticas — leitura por temática",
    f"Resultados · {NT}, itens 5.8 a 5.12",
    "O que está coberto e o que falta",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-3">
    <div class="leg-row">
      <span><i class="sw" style="background:{C_ATD};"></i>Atendida</span>
      <span><i class="sw" style="background:{C_CNV};"></i>Conversível</span>
      <span><i class="sw" style="background:{C_NOV};"></i>Novo ciclo</span>
      <span><i class="sw" style="background:{C_ART};"></i>Articulação</span>
      <span><i class="sw" style="background:{C_FORA};"></i>Sem método / fora</span>
    </div>
    <div class="flex-1 grid grid-cols-2 gap-4">
      <div class="tema">
        <p class="tema-t"><i class="fas fa-chart-line"></i> Diagnóstico do desempenho das APs</p>
        <div style="--rot:0px;">{_mini(3, 3, 2, 0, 0)}</div>
        <p><b style="color:{C_ATD};">Atendidas (3):</b> produtividade de terminais de contêineres; pátios de triagem; integração multimodal.</p>
        <p><b style="color:{C_CNV};">Conversíveis (3):</b> indicadores de produtividade, de serviço adequado e de qualidade — dados já coletados.</p>
        <p><b style="color:{C_NOV};">Novo ciclo (2):</b> participação dos usuários na revisão tarifária; Cartilha de Direitos dos Usuários.</p>
      </div>
      <div class="tema">
        <p class="tema-t"><i class="fas fa-building-shield"></i> Estrutura de fiscalização das APs</p>
        <div style="--rot:0px;">{_mini(2, 0, 0, 0, 2)}</div>
        <p><b style="color:{C_ATD};">Em análise (2):</b> fiscalização em portos concedidos; envio tempestivo de informações.</p>
        <p><b style="color:{C_FORA};">Sem método (2):</b> canal de acesso concedido; desempenho técnico da AP.
        Proposta: articular com o GT do <strong>tema 2.8 da Agenda Regulatória</strong>.</p>
      </div>
      <div class="tema">
        <p class="tema-t"><i class="fas fa-box"></i> Preço em terminais de contêineres</p>
        <div style="--rot:0px;">{_mini(5, 0, 7, 0, 4)}</div>
        <p><b style="color:{C_ATD};">Atendidas (5):</b> escaneamento; transparência de taxas; conceito de agente; matriz de risco da armazenagem; Res. ANTAQ nº 109/2023.</p>
        <p><b style="color:{C_NOV};">Novo ciclo (7):</b> caução por sobre-estadia; qualidade; informação de cobranças; retenção de carga; recusa de embarque; rastreabilidade; liberação documental.</p>
        <p><b style="color:{C_FORA};">Fora (4):</b> abusividade de preços e de sobre-estadia e sua natureza jurídica (juízo de mérito); oferta de contêineres (agente não alcançado).</p>
      </div>
      <div class="tema">
        <p class="tema-t"><i class="fas fa-ship"></i> Contabilização de TPB no REB</p>
        <div style="--rot:0px;">{_mini(1, 0, 0, 4, 0)}</div>
        <p><b style="color:{C_ATD};">Atendida (1):</b> contabilização do TPB para inscrição no REB.</p>
        <p><b style="color:{C_ART};">Articulação (4):</b> afretamento por tempo; consulta ao mercado; outorgas na navegação; fim de cobertura de bandeira.
        Dependem de método construído com a <strong>GRAT, a GAF e a GOA</strong>.</p>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">GRAT: Gerência de Recursos e de Apoio Técnico (SFC) · GAF e GOA: Gerências de Afretamento e de Outorgas de Autorização (SOG). Fonte: {NT}, itens 5.8 a 5.12.</p>
""",
    extra_css="""
.tema { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:14px 20px; display:flex; flex-direction:column; gap:8px; }
.tema .bar-row { grid-template-columns: 0 1fr; gap:0; }
.tema .bar-trk { height:26px; }
.tema p { margin:0; color:#475569; font-size:calc(15px * var(--tz)); line-height:1.45; }
.tema p.tema-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(19px * var(--tz)); }
.tema-t i { color:#0066CC; margin-right:6px; }
""",
    tag=TAG_TEMA,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 13 — Proposta: manter quatro, substituir três
# ---------------------------------------------------------------------------
slide(
    13,
    "Temáticas — proposta para o PAF 2027",
    f"Proposta PAF 2027 · {NT}, itens 6.1 a 6.3",
    "Manter quatro, substituir três",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="flex-1 grid grid-cols-12 gap-6">
      <div class="col-span-7 flex flex-col gap-3">
        <p class="titulo-sec"><i class="fas fa-circle-check" style="color:#15803D;"></i> Manter, com escopo ajustado</p>
        <div class="prop">
          <span class="prop-n">I</span>
          <div><p class="card-t">Diagnóstico do desempenho das APs</p>
          <p class="card-d">6 blocos, 17 demandas. Absorve 2 matérias de novo ciclo e 3 conversíveis; avalia APs ainda não fiscalizadas e retoma as avaliações mais antigas.</p></div>
        </div>
        <div class="prop">
          <span class="prop-n">II</span>
          <div><p class="card-t">Estrutura de fiscalização das APs</p>
          <p class="card-d">Instituições restantes; articulação com o GT do tema 2.8 da Agenda Regulatória para as matérias sem método.</p></div>
        </div>
        <div class="prop">
          <span class="prop-n">III</span>
          <div><p class="card-t">Diagnóstico dos Convênios de Delegação</p>
          <p class="card-d">Convênios restantes; mantida pela articulação com a fiscalização em curso do <strong>TCU</strong>, não pelo volume de demandas.</p></div>
        </div>
        <div class="prop" style="border-color:#FDE68A; background:#FFFBEB;">
          <span class="prop-n" style="background:#D97706;">IV</span>
          <div><p class="card-t">Serviços em terminais de contêineres <span class="pill pill-gold">novo nome</span></p>
          <p class="card-d">Hoje &ldquo;Preço em terminais de contêineres&rdquo;: maior alcance do conjunto (36 demandas) e 7 das 9 matérias de novo ciclo.</p></div>
        </div>
      </div>

      <div class="col-span-5 flex flex-col gap-3">
        <p class="titulo-sec"><i class="fas fa-arrow-right-arrow-left" style="color:#B91C1C;"></i> Substituir</p>
        <div class="card card-red">
          <div><p class="card-t">Transporte misto · Atraso e omissão de navios de contêineres</p>
          <p class="card-d">O universo de regulados permite concluir já neste ciclo, sem repetição no curto prazo.</p></div>
        </div>
        <div class="card card-red">
          <div><p class="card-t">Contabilização de TPB no REB</p>
          <p class="card-d">Eliminar ou suceder por tema de afretamento (outorgas e critérios), com o mesmo universo de regulados e o acervo já constituído.</p></div>
        </div>
        <div class="destaque">
          <p class="font-montserrat font-bold" style="font-size:calc(19px * var(--tz));">Por que &ldquo;Serviços&rdquo; e não &ldquo;Preço&rdquo;</p>
          <p class="text-blue-100 text-base mt-1">6 das 7 matérias pendentes tratam das <strong>condições de prestação</strong>:
          qualidade, tempestividade, rastreabilidade, continuidade e isonomia. O preço passa a ser uma dimensão —
          a cobrança e a transparência tarifária continuam integralmente apuradas, e afasta-se a leitura restritiva do escopo pelos regulados.</p>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-4 conta">
      <i class="fas fa-scale-balanced text-accent text-2xl"></i>
      <p><strong>Quantidade mantida em 7 temáticas</strong>, pela capacidade operacional da equipe e a complexidade dos temas:
      <span class="pill pill-a">4 mantidas</span> + <span class="pill pill-gold">3 vagas</span> a preencher na próxima etapa.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Reperfilamento: Lei nº 12.815/2013, art. 3º, II; Lei nº 10.233/2001, art. 20, II, &ldquo;a&rdquo;. Fonte: {NT}, itens 6.1, 6.2 e 6.3.</p>
""",
    extra_css="""
.prop { display:flex; gap:16px; align-items:flex-start; background:#F0FDF4; border:1px solid #BBF7D0; border-radius:14px; padding:12px 18px; }
.prop p { margin:0; }
.prop-n {
  min-width:44px; height:44px; border-radius:12px; background:#15803D; color:#fff; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(18px * var(--tz));
}
.conta { background:#F8FAFC; border-radius:14px; padding:12px 20px; }
.conta p { margin:0; color:#334155; font-size:calc(17px * var(--tz)); }
""",
    tag=TAG_TEMA,
    base=1.49,
)

# ---------------------------------------------------------------------------
# 14 — Recorte inicial: APs e convênios
# ---------------------------------------------------------------------------
def _chips(nomes, sel=()):
    return "".join(f'<span class="chip{" chip-on" if n in sel else ""}">{n}</span>' for n in nomes)

_sel_ap = ("Portos RS", "SUAPE", "Docas PB", "SCPAR Laguna", "CDSS")
_aps = [
    ("2026", ["APPA", "VPORTS", "SCPAR Imbituba", "SOPH", "CDSA"]),
    ("2025", ["Portos RIO", "CODERN", "CDC", "SNPH", "Porto de Recife"]),
    ("2024", ["CODEBA", "CDP", "EMAP"]),
    ("2023", ["APS", "Portos RS", "SUAPE"]),
    ("2022", ["Docas PB", "SCPAR São Francisco do Sul"]),
    ("Nunca", ["SCPAR Laguna", "CDSS"]),
]
_linhas_ap = "\n".join(
    f'<div class="ano-row"><span class="ano">{a}</span><div class="chips">{_chips(ns, _sel_ap)}</div></div>'
    for a, ns in _aps
)
slide(
    14,
    "Temáticas — recorte inicial",
    f"Proposta PAF 2027 · {NT}, itens 6.1.2 a 6.1.5",
    "Quem será avaliado no novo ciclo",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-3">
    <p class="sub-sec" style="font-size:calc(17px * var(--tz));">Critérios: <strong>antiguidade</strong> da última avaliação e <strong>desconcentração</strong> —
    evitar duas ações sobre a mesma Unidade Regional e a mesma localidade no mesmo exercício.
    <span class="chip chip-on" style="margin-left:8px;">em destaque: recorte inicial 2027</span></p>
    <div class="flex-1 grid grid-cols-2 gap-6">
      <div class="painel">
        <p class="titulo-sec">Autoridades Portuárias <span class="text-gray-400">· 20 acompanhadas</span></p>
        <p class="sub-sec mb-2">diagnóstico do desempenho, por ano da última avaliação</p>
        {_linhas_ap}
        <div class="card card-amber mt-3">
          <div><p class="card-d"><strong>APS e SCPAR São Francisco do Sul</strong>, embora antigas, ficam fora do recorte inicial:
          são das mesmas URs (GREST e GREFL) de CDSS e SCPAR Laguna, prioritárias por nunca terem sido avaliadas.</p></div>
        </div>
      </div>
      <div class="painel">
        <p class="titulo-sec">Convênios de Delegação <span class="text-gray-400">· 19 acompanhados</span></p>
        <p class="sub-sec mb-2">15 nunca foram avaliados</p>
        <div class="ano-row"><span class="ano" style="font-size:calc(14px * var(--tz));">Avaliados<br/>em 2026</span><div class="chips">{_chips(["São Francisco do Sul", "São Sebastião", "Pelotas", "Porto Alegre"])}</div></div>
        <div class="ano-row"><span class="ano" style="font-size:calc(14px * var(--tz));">Recorte<br/>2027 (12)</span><div class="chips">{_chips(["Imbituba", "Itaqui", "Recife", "Antonina", "Paranaguá", "Cachoeira do Sul", "Rio Grande", "Porto Velho", "Itajaí", "Macapá", "Forno", "Manaus"], ("Imbituba", "Itaqui", "Recife", "Antonina", "Paranaguá", "Cachoeira do Sul", "Rio Grande", "Porto Velho", "Itajaí", "Macapá", "Forno", "Manaus"))}</div></div>
        <div class="ano-row"><span class="ano" style="font-size:calc(14px * var(--tz));">Etapa<br/>posterior (3)</span><div class="chips">{_chips(["Suape", "Laguna", "Cabedelo"])}</div></div>
        <div class="card mt-3">
          <div><p class="card-d"><strong>Suape, Laguna e Cabedelo</strong> aguardam porque suas localidades já estão no recorte
          do diagnóstico de desempenho das APs em 2027.</p></div>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fundamento: Regimento Interno, art. 4º, XXXVII, e art. 84, II, &ldquo;a&rdquo;. Fonte: {NT}, itens 6.1.1, I, e 6.1.2 a 6.1.5; Quadros 4 e 5.</p>
""",
    extra_css="""
.painel { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:16px 22px; display:flex; flex-direction:column; gap:8px; }
.painel p { margin:0; }
.ano-row { display:grid; grid-template-columns:110px 1fr; align-items:center; gap:12px; padding:5px 0; border-bottom:1px solid #F1F5F9; }
.ano { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(17px * var(--tz)); line-height:1.15; }
.chips { display:flex; flex-wrap:wrap; gap:6px; }
.chip { display:inline-block; padding:4px 12px; border-radius:8px; background:#F1F5F9; color:#475569; font-size:calc(14.5px * var(--tz)); font-weight:600; }
.chip-on { background:#003366; color:#FFD700; }
""",
    tag=TAG_TEMA,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 15 — Três vagas: candidatos e consulta às URs
# ---------------------------------------------------------------------------
slide(
    15,
    "Temáticas — candidatos às três vagas",
    f"Proposta PAF 2027 · {NT}, itens 5.13 a 6.5 e 7",
    "Candidatos às três vagas",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-6 flex flex-col gap-3">
      <p class="titulo-sec">Ancorados na Agenda Regulatória <span class="text-gray-400">· 37 demandas</span></p>
      <table class="tbl">
        <thead><tr><th>Tema</th><th class="num">Dem.</th><th>Agenda Regulatória</th><th>Estudos</th></tr></thead>
        <tbody>
          <tr><td><strong>Agentes intermediários</strong> na cadeia de contêineres</td><td class="num">13</td><td>2.5 · não iniciado (2027)</td><td>P14 · a iniciar</td></tr>
          <tr><td><strong>Navegação interior</strong> em estiagem severa</td><td class="num">4</td><td>sem tema relacionado</td><td>P6 (indireto) · concluído</td></tr>
          <tr><td><strong>Pátios de triagem</strong> e acessos ao porto organizado</td><td class="num">2</td><td>3.5 · não iniciado (2026)</td><td>P1 · em andamento</td></tr>
          <tr style="background:#FFFBEB;"><td><strong>Apoio marítimo</strong>: outorgas e afretamento</td><td class="num"><strong>18</strong></td><td>2.7 · fase inicial; 2.4 · não iniciado</td><td>P21, P17 e P27</td></tr>
        </tbody>
      </table>
      <p class="legenda">Matéria regulatória em fase inicial ou estudo não concluído: a fiscalização gera <strong>evidência de campo</strong>
      aproveitável, sem sobrepor trabalho avançado. Apoio marítimo é o maior bloco da consulta, hoje apurado só no TPB.</p>

    </div>

    <div class="col-span-6 flex flex-col gap-2">
      <p class="titulo-sec">Reuniões de avaliação e Superintendências finalísticas</p>
      <div class="cand cand-c"><span>I</span>Recepção de resíduos de embarcações e reporte de dados ambientais</div>
      <div class="cand cand-c"><span>II</span>Inovação e cibersegurança das Autoridades Portuárias</div>
      <div class="cand cand-c"><span>III</span>Reincidência e efetividade das penalidades na navegação interior</div>
      <div class="cand"><span>IV</span>Transparência aos usuários, com expansão a TUPs e arrendamentos</div>
      <div class="cand"><span>V</span>Transporte marítimo de animais vivos e planos de contingência</div>
      <div class="cand"><span>VI</span>Retirada de resíduos de embarcações: efetividade e rastreabilidade</div>
      <div class="cand"><span>VII</span>Produtividade de arrendamentos</div>
      <div class="cand"><span>VIII</span>Manutenção de infraestruturas terrestres nos portos organizados</div>
      <div class="cand"><span>IX</span>Equipamentos e forma de embarque e desembarque de granel sólido</div>
      <p class="legenda mt-1"><span class="pill pill-gold">I a III</span> alcançam blocos <strong>sem cobertura</strong> em qualquer instrumento (complementaridade).
      I e VI incidem sobre o mesmo objeto: apreciar em conjunto, para temática única ou delimitação expressa.</p>

      <div class="consulta">
        <p class="card-t"><i class="fas fa-building-columns text-accent"></i> 10 matérias das Superintendências finalísticas</p>
        <div class="grid grid-cols-5 gap-2 mt-2">
          <div class="mt"><b>2</b><span>execução imediata — viraram os temas IV e VI ao lado</span></div>
          <div class="mt"><b>1</b><span>já contemplada na fiscalização de contêineres</span></div>
          <div class="mt"><b>2</b><span>para o GEF Investimentos</span></div>
          <div class="mt"><b>2</b><span>condicionadas a MAPA/ANVISA ou método conjunto</span></div>
          <div class="mt"><b>3</b><span>dependem de método — sem descarte</span></div>
        </div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">GEF: Grupo Especializado de Fiscalização. Fonte: {NT}, itens 5.13 a 5.17, 6.3 a 6.5 e Quadros 3 e 6.</p>
""",
    extra_css="""
.cand { display:flex; align-items:center; gap:14px; background:#F8FAFC; border-radius:10px; padding:6px 14px;
  color:#334155; font-size:calc(17px * var(--tz)); line-height:1.3; }
.cand span { min-width:40px; font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(15px * var(--tz)); }
.cand-c { background:#FFFBEB; border:1px solid #FDE68A; }
.consulta { background:#F8FAFC; border-radius:14px; padding:12px 16px; }
.consulta p { margin:0; }
.mt { background:#fff; border:1px solid #E2E8F0; border-radius:10px; padding:8px 10px; display:flex; flex-direction:column; gap:2px; }
.mt b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(26px * var(--tz)); line-height:1; }
.mt span { color:#64748B; font-size:calc(14.5px * var(--tz)); line-height:1.3; }
""",
    tag=TAG_TEMA,
    base=1.28,
)


# ===========================================================================
# VISÃO GERAL
# ===========================================================================
NTM = "minuta da NT de Metodologia do PAF 2027 (rodada de validação de 29/09/2026)"

slide(
    2,
    "PAF 2027 — duas frentes",
    "Apresentação ao Diretor-Geral · 2 de outubro de 2026",
    "O PAF 2027 em duas frentes",
    """
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="flex-1 grid grid-cols-2 gap-6">
      <div class="frente">
        <div class="frente-top" style="background:linear-gradient(135deg,#7F1D1D,#B91C1C);">
          <i class="fas fa-gauge-high"></i>
          <div><p class="frente-k">Bloco 1</p><p class="frente-t">Fiscalizações do grupo de risco</p></div>
        </div>
        <div class="frente-body">
          <p class="frente-q">Quem fiscalizar, e com que intensidade?</p>
          <p>Cada outorga recebe uma nota de risco (<strong>IPR 2.0</strong>) e uma faixa de A1 a C4.
          A faixa define a ação: presencial no Grupo C, remota no B, sorteio no A.</p>
          <div class="grid grid-cols-3 gap-3 mt-1">
            <div class="kpi"><b>2.466</b><span>outorgas avaliadas</span></div>
            <div class="kpi"><b>&asymp;669</b><span>no PAF 2027</span></div>
            <div class="kpi"><b>45,9 mil</b><span>horas · 83% da capacidade</span></div>
          </div>
          <p class="frente-f"><i class="fas fa-file-lines"></i> Minuta da NT de Metodologia do PAF 2027 · IPR 2.0 (NT 11, 12, 19 e 20/2026)</p>
        </div>
      </div>

      <div class="frente">
        <div class="frente-top" style="background:linear-gradient(135deg,#003366,#0066CC);">
          <i class="fas fa-layer-group"></i>
          <div><p class="frente-k">Bloco 2</p><p class="frente-t">Fiscalizações temáticas</p></div>
        </div>
        <div class="frente-body">
          <p class="frente-q">Que problema do setor examinar a fundo?</p>
          <p>Ações transversais sobre um tema, e não sobre uma outorga. Para 2027, a escolha partiu das
          <strong>99 contribuições</strong> da revisão da Agenda Regulatória, como pede a Deliberação-DG nº 96/2025.</p>
          <div class="grid grid-cols-3 gap-3 mt-1">
            <div class="kpi"><b>7</b><span>temáticas (quantidade mantida)</span></div>
            <div class="kpi"><b>4</b><span>mantidas, com escopo ajustado</span></div>
            <div class="kpi"><b>3</b><span>vagas a preencher</span></div>
          </div>
          <p class="frente-f"><i class="fas fa-file-lines"></i> Nota Técnica nº 27/2026/GPF/SFC · SEI 3024667</p>
        </div>
      </div>
    </div>

    <div class="crono">
      <p class="titulo-sec mb-2">Calendário até a Diretoria Colegiada</p>
      <div class="grid grid-cols-5 gap-3">
        <div class="marco feito"><b>29/09</b><span>Rodada de validação do IPR e equalização aprovada</span></div>
        <div class="marco feito"><b>30/09</b><span>Data de referência do ciclo 2027 (corte cadastral)</span></div>
        <div class="marco hoje"><b>02/10 · hoje</b><span>Encerra a consulta técnica às Unidades Regionais</span></div>
        <div class="marco"><b>Outubro</b><span>Extração oficial com o sorteio do Grupo A, consolidação e escolha das 3 temáticas</span></div>
        <div class="marco"><b>Até 31/10</b><span>Proposta do PAF 2027 submetida à Diretoria Colegiada</span></div>
      </div>
    </div>
  </div>
""",
    extra_css="""
.frente { border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; display:flex; flex-direction:column; }
.frente-top { color:#fff; padding:16px 24px; display:flex; align-items:center; gap:16px; }
.frente-top i { font-size:calc(30px * var(--tz)); opacity:0.9; }
.frente-top p { margin:0; }
.frente-k { font-family:'Montserrat',sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.12em; font-size:calc(13px * var(--tz)); opacity:0.8; }
.frente-t { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(26px * var(--tz)); }
.frente-body { flex:1; padding:18px 24px; display:flex; flex-direction:column; justify-content:space-between; gap:10px; }
.frente-body p { margin:0; color:#475569; font-size:calc(17px * var(--tz)); line-height:1.5; }
.frente-body strong { color:#003366; }
.frente-body p.frente-q { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(22px * var(--tz)); }
.frente-body p.frente-f { color:#94A3B8; font-size:calc(13.5px * var(--tz)); }
.kpi { background:#F8FAFC; border-radius:12px; padding:10px 14px; display:flex; flex-direction:column; }
.kpi b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(30px * var(--tz)); line-height:1.1; }
.kpi span { color:#64748B; font-size:calc(14px * var(--tz)); }
.crono { background:#F8FAFC; border-radius:16px; padding:14px 20px; }
.crono p { margin:0; }
.marco { border-top:5px solid #CBD5E1; padding-top:8px; display:flex; flex-direction:column; gap:3px; }
.marco b { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(19px * var(--tz)); }
.marco span { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.35; }
.marco.feito { border-top-color:#0066CC; }
.marco.hoje { border-top-color:#FFD700; }
.marco.hoje b { color:#92400E; }
""",
    tag=TAG_GERAL,
    base=1.61,
)


# ===========================================================================
# BLOCO 1 — FISCALIZAÇÕES DO GRUPO DE RISCO (IPR 2.0)
# ===========================================================================

# Colunas das faixas: um matiz por grupo (verde A, azul B, vermelho C), com o tom
# escurecendo dentro do grupo conforme a intensidade da ação. Rótulo direto em cada coluna.
_FAIXAS = [
    ("A1", 272, "monitoramento", "#4ADE80"), ("A2", 159, "monitoramento", "#16A34A"),
    ("B1", 906, "documental", "#60A5FA"), ("B2", 502, "à distância", "#1D4ED8"),
    ("C1", 286, "programada", "#F87171"), ("C2", 194, "sem aviso", "#EF4444"),
    ("C3", 77, "intensiva", "#B91C1C"), ("C4", 30, "intervenção", "#7F1D1D"),
]


def _colunas_faixa():
    vmax = 1000
    grade = "".join(
        f'<div class="cc-grid" style="bottom:{100 * g / vmax:.1f}%;"></div>' for g in (250, 500, 750)
    )
    cols = "".join(
        f'<div class="cc-col" title="{f}: {v} outorgas">'
        f'<div class="cc-b" style="height:{100 * v / vmax:.2f}%;background:{cor};"></div>'
        f'<div class="cc-v" style="bottom:calc({100 * v / vmax:.2f}% + 8px);">{v:,}</div></div>'.replace(",", ".")
        for f, v, _, cor in _FAIXAS
    )
    eixo = "".join(f"<div><b>{f}</b><span>{sol}</span></div>" for f, _, sol, _ in _FAIXAS)
    return f"""
      <div class="cc">
        <div class="cc-plot">{grade}{cols}</div>
        <div class="cc-x">{eixo}</div>
        <div class="cc-g">
          <div style="grid-column:span 2; border-color:#16A34A;"><strong>Grupo A</strong> · menor risco<br/>monitoramento e <strong>sorteio auditável</strong> · 431</div>
          <div style="grid-column:span 2; border-color:#1D4ED8;"><strong>Grupo B</strong> · intermediário<br/>ação <strong>remota</strong> · 1.408</div>
          <div style="grid-column:span 4; border-color:#B91C1C;"><strong>Grupo C</strong> · maior risco<br/>ação <strong>presencial</strong>, até intervenção técnica com possível cautelar · 587</div>
        </div>
      </div>"""


# ---------------------------------------------------------------------------
# 03 — Do risco à solução fiscal
# ---------------------------------------------------------------------------
slide(
    3,
    "Grupo de risco — do risco à ação fiscal",
    "Fiscalização Responsiva · PPF 2025-2028",
    "Do risco à ação fiscal",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-5 flex flex-col gap-3">
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(24px * var(--tz));">Índice de Perfil de Risco (IPR)</p>
        <p class="text-blue-100 text-lg mt-1">Cada outorga recebe uma <strong>nota de 0 a 100</strong> e uma
        <strong>faixa de A1 a C4</strong>. A intensidade da ação fiscal é proporcional ao risco — é o modelo
        de Fiscalização Responsiva do PPF 2025-2028.</p>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-file-signature text-accent text-2xl"></i></div>
        <div><p class="card-t">A unidade é a outorga, não a empresa</p>
        <p class="card-d">Uma EBN com quatro linhas de travessia tem quatro IPRs: o risco de uma travessia no
        Oiapoque não é o de outra em Manaus.</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-scale-balanced text-accent text-2xl"></i></div>
        <div><p class="card-t">A nota mistura duas coisas</p>
        <p class="card-d"><strong>O que a empresa já fez</strong> (autuações, reincidência, NoCI descumprida, denúncias
        que viraram sanção) e <strong>o que ela é</strong> (risco da atividade, porte, acesso, maturidade e há quanto
        tempo ninguém a visita).</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-user-check text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">O índice prioriza; a chefia decide</p>
        <p class="card-d">O IPR indica a ordem, sem substituir o juízo técnico: toda inclusão ou exclusão fora da regra
        fica registrada, com autor e fundamento.</p></div>
      </div>
    </div>

    <div class="col-span-7 flex flex-col gap-3">
      <div>
        <p class="titulo-sec">Outorgas por faixa e a solução fiscal de cada uma</p>
        <p class="sub-sec">2.426 outorgas ativas no ciclo 2027 (2.466 do universo, menos 40 com CNPJ baixado ou suspenso)</p>
      </div>
      {_colunas_faixa()}
      <p class="legenda">A correspondência faixa &rarr; solução fiscal é parametrizada e versionada, não fixada em programa.
      A navegação marítima é documental em qualquer faixa (61 outorgas do Grupo C).</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {NTM}, Quadro 2.</p>
""",
    extra_css="""
.cc { display:flex; flex-direction:column; flex:1; }
.cc-plot { position:relative; flex:1; min-height:calc(240px * var(--tz)); display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; align-items:stretch; border-bottom:2px solid #94A3B8; padding:0 6px; }
.cc-grid { position:absolute; left:0; right:0; border-top:1px dashed #E2E8F0; }
.cc-col { position:relative; z-index:1; }
.cc-v { position:absolute; left:-8px; right:-8px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; color:#0F172A; font-size:calc(22px * var(--tz)); line-height:1; }
.cc-b { position:absolute; left:0; right:0; bottom:0; border-radius:6px 6px 0 0; }
.cc-x { display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; padding:8px 6px 0; }
.cc-x div { text-align:center; line-height:1.2; }
.cc-x b { display:block; font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(19px * var(--tz)); }
.cc-x span { color:#64748B; font-size:calc(13.5px * var(--tz)); }
.cc-g { display:grid; grid-template-columns:repeat(8,1fr); column-gap:16px; padding:10px 6px 0; }
.cc-g div { border-top:4px solid; padding-top:6px; text-align:center; color:#475569; font-size:calc(15px * var(--tz)); line-height:1.3; }
.cc-g strong { color:#003366; font-family:'Montserrat',sans-serif; }
""",
    tag=TAG_RISCO,
    base=1.45,
)

# ---------------------------------------------------------------------------
# 04 — IPR 2.0: o que a nota passou a enxergar
# ---------------------------------------------------------------------------
slide(
    4,
    "Grupo de risco — IPR 2.0",
    "IPR 2.0 · NT 11, 12, 19 e 20/2026",
    "O que a nota passou a enxergar",
    f"""
  <div class="flex-1 px-16 pb-2 flex flex-col gap-4">
    <div class="grid grid-cols-12 gap-6">
      <div class="col-span-7 card card-red" style="align-items:center;">
        <div class="ico" style="background:#FECACA;"><i class="fas fa-eye-slash text-red-700 text-2xl"></i></div>
        <div>
          <p class="card-t">O defeito que motivou a revisão</p>
          <p class="card-d">Os seis indicadores da NT 9/2021 dependem de fiscalização anterior. Quem nunca foi fiscalizado
          marcava zero em tudo e caía em A1: <strong>quanto menos a Agência olhava, mais segura a outorga parecia.</strong></p>
        </div>
      </div>
      <div class="col-span-5 grid grid-cols-2 gap-3">
        <div class="stat-card"><p class="stat-num">595</p><p class="text-blue-200 text-sm font-semibold mt-2">outorgas nunca<br/>fiscalizadas</p></div>
        <div class="stat-card"><p class="stat-num">38%</p><p class="text-blue-200 text-sm font-semibold mt-2">do universo sem visita<br/>há mais de 5 anos ou nunca</p></div>
      </div>
    </div>

    <div class="flex-1 grid grid-cols-5 gap-3">
      <div class="ind">
        <div class="ind-h"><span class="ind-s">ICF</span><span class="ind-p">peso 3</span></div>
        <p class="ind-t">Há quanto tempo ninguém olha</p>
        <p>Nota sobe com o tempo desde a última fiscalização; nunca visitada leva a máxima. Fiscalizou, a nota zera e a outorga dá lugar a outra.</p>
      </div>
      <div class="ind">
        <div class="ind-h"><span class="ind-s">IVO</span><span class="ind-p">peso 2</span></div>
        <p class="ind-t">O porte da operação</p>
        <p>Volume comparado com pares da mesma categoria. Só pesa quando ninguém está olhando: IVO efetivo = IVO &times; ICF.</p>
      </div>
      <div class="ind">
        <div class="ind-h"><span class="ind-s">ICD</span><span class="ind-p">peso 1</span></div>
        <p class="ind-t">Custo de chegar lá</p>
        <p>Desde setembro, mede a <strong>via real</strong> usada nas viagens da Agência (viatura, barco ou avião), não a linha reta.</p>
      </div>
      <div class="ind">
        <div class="ind-h"><span class="ind-s">IMA</span><span class="ind-p">peso 1</span></div>
        <p class="ind-t">Quem opera</p>
        <p>Idade do CNPJ e porte: empresa jovem e pequena tende a ter menos estrutura de conformidade. Priorização, não punição.</p>
      </div>
      <div class="ind" style="border-top-color:#D97706;">
        <div class="ind-h"><span class="ind-s" style="color:#B45309;">F_IRA</span><span class="ind-p">piso</span></div>
        <p class="ind-t">O risco da atividade</p>
        <p>Atividade perigosa tem nota mínima: uma travessia nunca fiscalizada <strong>jamais cai em A1</strong>.</p>
      </div>
    </div>

    <div class="formula" style="text-align:center; line-height:1.7;">
      IPR = MAIOR( nota comportamental e de exposição ponderada <span style="color:#94A3B8;">(&Sigma; pesos = 21)</span> , piso da atividade )<br/>
      <span style="color:#94A3B8; font-size:calc(16px * var(--tz));">Faixas A1..C4 recalibradas ao universo real (nota máxima 54,79) e à capacidade de fiscalizar · réguas versionadas em tabela</span>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Números do universo do ciclo 2027 (2.466 outorgas), painel IPR-PAF em 01/10/2026. Fonte: NT 11/2026 e 12/2026, revisadas pelas NT 19/2026 e 20/2026; {NTM}, item 2.</p>
""",
    extra_css="""
.ind { background:#F8FAFC; border-top:5px solid #0066CC; border-radius:12px; padding:18px 18px; display:flex; flex-direction:column; justify-content:center; gap:10px; }
.ind p { margin:0; color:#475569; font-size:calc(17.5px * var(--tz)); line-height:1.45; }
.ind p.ind-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(20px * var(--tz)); }
.ind-h { display:flex; justify-content:space-between; align-items:baseline; }
.ind-s { font-family:'Montserrat',sans-serif; font-weight:900; color:#0066CC; font-size:calc(32px * var(--tz)); }
.ind-p { color:#94A3B8; font-size:calc(13px * var(--tz)); font-weight:600; text-transform:uppercase; letter-spacing:0.06em; }
""",
    tag=TAG_RISCO,
    base=1.5,
)

# ---------------------------------------------------------------------------
# 05 — O que entra no PAF 2027
# ---------------------------------------------------------------------------
slide(
    5,
    "Grupo de risco — composição do PAF 2027",
    "Composição · regra por grupo, não número fixo",
    "O que entra no PAF 2027",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-7 flex flex-col gap-3">
      <div class="comp comp-c">
        <div class="comp-n">587</div>
        <div><p class="card-t"><span class="pill pill-c">Grupo C</span> &nbsp;entra inteiro</p>
        <p class="card-d">As outorgas de maior risco. Fiscalizá-las é obrigação do modelo, não escolha de escopo: o Grupo C é o <strong>piso</strong> do plano.</p></div>
      </div>
      <div class="comp comp-b">
        <div class="comp-n">52</div>
        <div><p class="card-t"><span class="pill pill-b">Grupo B</span> &nbsp;entra na medida do que cabe</p>
        <p class="card-d">Das 1.408, as primeiras do ranking até o limite da força de trabalho. Ordem estrita: não se pula uma outorga de maior risco para incluir outra que caberia.</p></div>
      </div>
      <div class="comp comp-a">
        <div class="comp-n">&asymp;30</div>
        <div><p class="card-t"><span class="pill pill-a">Grupo A</span> &nbsp;entra por sorteio</p>
        <p class="card-d">Fração das 431 de menor risco — 10%, 7% ou 5% conforme o risco da atividade — para que ninguém fique fora do radar.</p></div>
      </div>
      <div class="destaque flex items-center gap-6">
        <p class="font-montserrat font-black" style="font-size:calc(54px * var(--tz)); line-height:1;">&asymp;669</p>
        <p class="text-blue-100 text-lg">outorgas e <strong>45.880 horas</strong>. Substitui o recorte informal de <strong>200 outorgas</strong> dos ciclos anteriores —
        inferior ao próprio Grupo C, que sozinho tem quase o triplo.</p>
      </div>
    </div>

    <div class="col-span-5 flex flex-col gap-3">
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-id-card text-accent text-2xl"></i></div>
        <div><p class="card-t">Todo CNPJ conferido na Receita Federal</p>
        <p class="card-d">49 outorgas com CNPJ baixado ou suspenso: <strong>40 saíram da lista</strong> e 9 ficaram por decisão
        fundamentada (sucessão já reconhecida). Nenhum bloqueio sem tratamento. Sair da lista não é sair do universo:
        a área de outorgas recebe o dossiê do CNPJ para decidir sobre o instrumento.</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-dice text-accent text-2xl"></i></div>
        <div><p class="card-t">Sorteio que qualquer um pode refazer</p>
        <p class="card-d">A Agência publica a lista de elegíveis e a sua impressão digital <strong>antes</strong> de conhecer
        a semente — um pulso futuro do <strong>NIST Randomness Beacon</strong>. Mesma lista + mesma semente = mesmas sorteadas.</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-hourglass-half text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">O sorteio roda na extração oficial</p>
        <p class="card-d">Junto com os demais dados do PAF: a Diretoria recebe o plano já com a lista nominal do Grupo A. Os &asymp;30 de hoje são o valor esperado.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Protocolos IPR-CADASTRO-V1 e IPR-SORTEIO-V1. Fonte: {NTM}, itens 3.2, 3.4 e 5.</p>
""",
    extra_css="""
.comp { display:flex; align-items:center; gap:22px; border-radius:14px; padding:12px 20px; border:1px solid; }
.comp p { margin:0; }
.comp-n { min-width:120px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(46px * var(--tz)); line-height:1; color:#003366; }
.comp-c { background:#FEF2F2; border-color:#FECACA; }
.comp-b { background:#EFF6FF; border-color:#BFDBFE; }
.comp-a { background:#F0FDF4; border-color:#BBF7D0; }
""",
    tag=TAG_RISCO,
    base=1.61,
)

# ---------------------------------------------------------------------------
# 06 — O plano cabe em quem o executa
# ---------------------------------------------------------------------------
def _ocup(nome, antes, depois):
    cor = "#B91C1C" if antes > 130 else "#C2410C"
    w_antes = min(antes, 400) / 400 * 100
    w_dep = depois / 400 * 100
    return f"""
      <div class="oc-row">
        <div class="oc-rot"><strong>{nome}</strong></div>
        <div class="oc-trk">
          <div class="oc-lim"></div>
          <div class="oc-bar" style="width:{w_antes:.1f}%; background:{cor}; opacity:0.28;"></div>
          <div class="oc-bar" style="width:{w_dep:.1f}%; background:#0066CC; top:9px; height:18px;"></div>
        </div>
        <div class="oc-val"><span style="color:{cor};">{antes}%</span> &rarr; <strong>{depois}%</strong></div>
      </div>"""

slide(
    6,
    "Grupo de risco — força de trabalho e equalização",
    "Força de trabalho · equalização entre unidades",
    "O plano cabe em quem o executa?",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-7 flex flex-col gap-3">
      <div class="formula" style="text-align:center; line-height:1.6;">
        ocupação = horas que o plano exige &divide; horas disponíveis para o PAF<br/>
        <span style="color:#94A3B8; font-size:calc(16px * var(--tz));">horas disponíveis = 35% das horas líquidas de cada fiscal no PGD (Hefesto), igual para toda unidade · inclui os 20 do CNU</span>
      </div>
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(22px * var(--tz));">Cabe na Agência, mas não cabe onde a carga está.</p>
        <p class="text-blue-100 text-lg mt-1">O plano exige <strong>45.880 h</strong> das <strong>55.560 h</strong> disponíveis: 83% no agregado nacional.
        Pela jurisdição, porém, quatro unidades passam do limite.</p>
      </div>
      <div>
        <p class="titulo-sec">Ocupação antes e depois da equalização</p>
        <div class="leg-row mt-1">
          <span><i class="sw" style="background:#B91C1C; opacity:0.28;"></i>pela jurisdição</span>
          <span><i class="sw" style="background:#0066CC;"></i>após a equalização aprovada</span>
          <span><i class="sw" style="background:#003366; width:3px;"></i>limite de 100%</span>
        </div>
      </div>
      {_ocup("URESN · Santana", 395, 96)}
      {_ocup("GREBL · Belém", 146, 100)}
      {_ocup("GREMN · Manaus", 123, 100)}
      {_ocup("UREPL", 105, 91)}
      <p class="legenda">Demais 10 unidades: de 23% a 88% antes; receptoras ficam entre 55% e 88% depois. Nenhuma receptora passa de 90%.</p>
    </div>

    <div class="col-span-5 flex flex-col gap-3">
      <div class="grid grid-cols-3 gap-3">
        <div class="stat-card"><p class="stat-num">30</p><p class="text-blue-200 text-sm font-semibold mt-2">movimentos<br/>(9.531 h)</p></div>
        <div class="stat-card"><p class="stat-num">8</p><p class="text-blue-200 text-sm font-semibold mt-2">transferências<br/>(765 h)</p></div>
        <div class="stat-card"><p class="stat-num">22</p><p class="text-blue-200 text-sm font-semibold mt-2">missões de apoio<br/>(7 campo · 15 remotas)</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-route text-accent text-2xl"></i></div>
        <div><p class="card-t">Oiapoque: uma ida só</p>
        <p class="card-d">56 travessias sob jurisdição de Santana: a <strong>URESL</strong> faz a vistoria e a <strong>GREST</strong> as fases de
        escritório (NT 2/2024 — só a Fase 2 exige ir ao local).</p></div>
      </div>
      <div class="card">
        <div class="ico" style="background:#DBEAFE;"><i class="fas fa-landmark text-accent text-2xl"></i></div>
        <div><p class="card-t">A jurisdição não muda</p>
        <p class="card-d">A equalização diz quem <strong>executa</strong> no ciclo, não quem <strong>responde</strong>. A regra propõe; cada movimento é aprovado com autor e fundamento.
        Os 30 foram aprovados em 29/09.</p></div>
      </div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-users text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">O limite é de lotação no Norte</p>
        <p class="card-d">GREBL e GREMN ficam exatamente em 100%. A cobertura do Grupo B (52 de 1.408, <strong>3,7%</strong>) só cresce com reforço nessas unidades.</p></div>
      </div>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Protocolos IPR-DIMENSIONA-V1 e IPR-EQUALIZA-V1. Fonte: {NTM}, itens 6 a 8 e Quadros 5 e 6.</p>
""",
    extra_css="""
.oc-row { display:grid; grid-template-columns:230px 1fr 170px; align-items:center; gap:14px; }
.oc-rot { color:#334155; font-size:calc(18px * var(--tz)); }
.oc-rot strong { color:#003366; }
.oc-trk { position:relative; height:36px; background:#F1F5F9; border-radius:4px; }
.oc-bar { position:absolute; left:0; top:0; height:36px; border-radius:0 4px 4px 0; }
.oc-lim { position:absolute; left:25%; top:-4px; bottom:-4px; width:3px; background:#003366; z-index:2; }
.oc-val { font-family:'Montserrat',sans-serif; font-size:calc(20px * var(--tz)); color:#003366; }
""",
    tag=TAG_RISCO,
    base=1.36,
)

# ---------------------------------------------------------------------------
# 07 — Deslocamento: quanto custa ir a campo
# ---------------------------------------------------------------------------
# Gasto real com viagens da ANTAQ (Portal da Transparência, publicação de 20/09/2026,
# viagens realizadas, diárias + passagens + outros gastos, valores nominais, R$ mil),
# classificadas com a régua do painel IPR-PAF (etl/transform/viagens_sfc.py): pessoa da
# SFC = planilha de controle da SFC ou grupo C revisado; fiscalização = pessoa da SFC
# com motivo fiscal. 2026 é parcial.
# (ano, ANTAQ, SFC, fiscalização da SFC)
_VIAG = [(2019, 2090, 1205, 262), (2020, 504, 346, 194), (2021, 1014, 719, 421),
         (2022, 2737, 1245, 594), (2023, 4033, 1735, 797), (2024, 3241, 1424, 585),
         (2025, 2568, 980, 435), (2026, 1186, 521, 160)]
_PAF_MIL = 218.5
C_FISC, C_SFC, C_RESTO = "#003366", "#5B9BD5", "#CBD5E1"


def _colunas_desloc():
    vmax = 4400
    grade = "".join(
        f'<div class="cc-grid" style="bottom:{100 * g / vmax:.1f}%;"><span>{g // 1000} mi</span></div>'
        for g in (1000, 2000, 3000, 4000)
    )
    cols = []
    for a, tot, sfc_, fis in _VIAG:
        op = "opacity:0.55;" if a == 2026 else ""
        segs = [(fis, C_FISC), (sfc_ - fis, C_SFC), (tot - sfc_, C_RESTO)]
        pilha = "".join(
            f'<div style="height:{100 * v / tot:.2f}%;background:{c};"></div>' for v, c in reversed(segs)
        )
        cols.append(
            f'<div class="cc-col" title="{a}: ANTAQ R$ {tot} mil · SFC R$ {sfc_} mil · fiscalização R$ {fis} mil">'
            f'<div class="cc-b dl-stack" style="height:{100 * tot / vmax:.2f}%;{op}">{pilha}</div>'
            f'<div class="cc-v" style="bottom:calc({100 * tot / vmax:.2f}% + 6px);">{tot:,}</div></div>'.replace(",", ".")
        )
    linha = f'<div class="dl-paf" style="bottom:{100 * _PAF_MIL / vmax:.2f}%;"></div>'
    eixo = "".join(
        f"<div><b>{a}</b>{'<span>parcial</span>' if a == 2026 else ''}</div>" for a, *_ in _VIAG
    )
    pct = lambda f: "".join(f"<div>{f(t, s_, x)}%</div>" for _, t, s_, x in _VIAG)
    return f"""
      <div class="cc s7">
        <div class="leg-row" style="margin-bottom:10px;">
          <span><i class="sw" style="background:{C_FISC};"></i>fiscalização (SFC)</span>
          <span><i class="sw" style="background:{C_SFC};"></i>demais viagens da SFC</span>
          <span><i class="sw" style="background:{C_RESTO};"></i>demais áreas da ANTAQ</span>
          <span><i class="sw" style="background:none; border-top:3px dashed #B45309; height:0; width:28px; border-radius:0;"></i><strong style="color:#92400E;">PAF 2027: R$ 218,5 mil</strong></span>
        </div>
        <div class="cc-plot">{grade}{"".join(cols)}{linha}</div>
        <div class="cc-x">{eixo}</div>
        <div class="dl-pct"><p>% da SFC</p><div class="dl-pr">{pct(lambda t, s_, x: round(100 * s_ / t))}</div></div>
        <div class="dl-pct"><p>% da fiscalização</p><div class="dl-pr dl-f">{pct(lambda t, s_, x: round(100 * x / t))}</div></div>
      </div>"""


slide(
    7,
    "Grupo de risco — custo de deslocamento",
    "Deslocamento · protocolo IPR-DESLOCA-V1",
    "Quanto custa ir a campo",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-12 gap-6">
    <div class="col-span-5 flex flex-col gap-3">
      <p class="titulo-sec">Como o custo foi estimado</p>
      <div class="passo"><b>501</b><span><strong>fiscalizações presenciais</strong>: o Grupo C sem a navegação marítima,
        que é documental (481), mais as &asymp;20 esperadas do sorteio do Grupo A.</span></div>
      <div class="passo"><b>160</b><span><strong>viagens</strong>: tudo o que uma unidade fiscaliza na mesma cidade vira uma só viagem.
        <strong>52</strong> ficam a até 120 km e vão de viatura, sem passagem.</span></div>
      <div class="passo"><b>108</b><span><strong>viagens pagas</strong>: dias e passagens pelo histórico real da ANTAQ no mesmo trajeto
        (Portal da Transparência, 2019-2026, passagens corrigidas pelo IPCA), diária do Decreto 5.992/2006 e equipe de 2 fiscais.</span></div>
      <div class="card card-amber">
        <div class="ico" style="background:#FDE68A;"><i class="fas fa-circle-info text-yellow-700 text-2xl"></i></div>
        <div><p class="card-t">A confiança do número fica à vista</p>
        <p class="card-d">36 viagens têm histórico do próprio trajeto; 72 usam a média da UF ou a média nacional por distância.
        Cada viagem guarda a origem da estimativa.</p></div>
      </div>
    </div>

    <div class="col-span-7 flex flex-col gap-3">
      <div class="grid grid-cols-3 gap-3">
        <div class="stat-card"><p class="stat-num sn-m">R$ 218,5 mil</p><p class="text-blue-200 text-base font-semibold mt-2">custo estimado do PAF presencial<br/>(diárias 129,6 + passagens 68,4)</p></div>
        <div class="stat-card"><p class="stat-num sn-m">R$ 436</p><p class="text-blue-200 text-base font-semibold mt-2">por fiscalização<br/>presencial</p></div>
        <div class="stat-card"><p class="stat-num sn-m">50%</p><p class="text-blue-200 text-base font-semibold mt-2">do que a SFC gastou em viagens<br/>de fiscalização em 2025</p></div>
      </div>
      <div>
        <p class="titulo-sec">Quanto a ANTAQ gasta com viagens, e quanto disso é fiscalização <span class="text-gray-400">· R$ mil</span></p>
        <p class="sub-sec">diárias, passagens e outros gastos das viagens realizadas · total da ANTAQ no topo de cada coluna</p>
      </div>
      {_colunas_desloc()}
      <p class="legenda">Em 2025, a SFC respondeu por <strong>38%</strong> do gasto da Agência com viagens e a fiscalização por <strong>17%</strong>.
      O PAF presencial equivale a <strong>36%</strong> da média de fiscalização de 2022-2025 (R$ 603 mil) e a <strong>9%</strong> do gasto total de 2025.
      O real inclui o que o PAF não programa: extraordinárias, denúncias e eventos sazonais.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Estimativa: painel IPR-PAF, rodada de deslocamento de 28/09/2026, e {NTM}, item 10. Gasto real: viagens realizadas da ANTAQ no Portal da
  Transparência (publicação de 20/09/2026), valores nominais; SFC = servidores da planilha de controle da SFC e fiscais revisados; fiscalização = viagem da SFC com motivo fiscal.</p>
""",
    extra_css="""
.passo { display:flex; align-items:center; gap:18px; background:#F8FAFC; border-radius:12px; padding:12px 18px; }
.passo b { min-width:84px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; color:#0066CC; font-size:calc(30px * var(--tz)); }
.passo span { color:#475569; font-size:calc(16px * var(--tz)); line-height:1.4; }
.passo strong { color:#003366; }
.cc { display:flex; flex-direction:column; flex:1; }
.cc-plot { position:relative; flex:1; min-height:calc(200px * var(--tz)); display:grid; grid-template-columns:repeat(8,1fr); column-gap:18px; align-items:stretch; border-bottom:2px solid #94A3B8; padding:0 6px; }
.cc-grid { position:absolute; left:0; right:0; border-top:1px dashed #E2E8F0; }
.cc-grid span { position:absolute; left:-2px; top:-18px; color:#94A3B8; font-size:12px; }
.cc-col { position:relative; z-index:1; }
.cc-v { position:absolute; left:-8px; right:-8px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:700; color:#0F172A; font-size:calc(16px * var(--tz)); line-height:1; }
.dl-stack { display:flex; flex-direction:column; gap:2px; overflow:hidden; }
.dl-stack div:last-child { flex:none; }
.dl-pct { display:grid; grid-template-columns:repeat(8,1fr); column-gap:18px; padding:6px 6px 0; position:relative; }
.dl-pct p { position:absolute; left:0; top:6px; margin:0; width:130px; color:#64748B; font-size:calc(13px * var(--tz)); line-height:1.2; }
.s7 .cc-plot, .s7 .cc-x, .s7 .dl-pct { padding-left:136px; }
.s7 .cc-grid, .s7 .dl-paf { left:130px; }
.s7 .cc-grid span { left:-46px; top:-8px; }
.dl-pr { display:contents; }
.dl-pr div { text-align:center; font-family:'Montserrat',sans-serif; font-weight:700; color:#5B9BD5; font-size:calc(15px * var(--tz)); }
.dl-pr.dl-f div { color:#003366; }
.cc-b { position:absolute; left:0; right:0; bottom:0; border-radius:6px 6px 0 0; }
.cc-x { display:grid; grid-template-columns:repeat(8,1fr); column-gap:18px; padding:8px 6px 0; }
.cc-x div { text-align:center; line-height:1.15; }
.cc-x b { display:block; font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(17px * var(--tz)); }
.cc-x span { color:#64748B; font-size:calc(13px * var(--tz)); }
.dl-paf { position:absolute; left:0; right:0; border-top:3px dashed #B45309; z-index:2; }
.slide .stat-num.sn-m { font-size:calc(40px * var(--tz)); }
.passo, .col-span-5 > .card { flex:1; }
""",
    tag=TAG_RISCO,
    base=1.26,
)


# ===========================================================================
# 16 — SÍNTESE E ENCAMINHAMENTOS
# ===========================================================================
slide(
    16,
    "Síntese e encaminhamentos",
    "Síntese",
    "O que vai à Diretoria Colegiada",
    f"""
  <div class="flex-1 px-16 pb-2 grid grid-cols-2 gap-6">
    <div class="enc">
      <div class="enc-top" style="background:linear-gradient(135deg,#7F1D1D,#B91C1C);"><i class="fas fa-gauge-high"></i> Grupo de risco</div>
      <div class="enc-body">
        <p><b>a</b><span><strong>Aprovar a metodologia</strong> de composição, dimensionamento, equalização e agendamento para o ciclo 2027.</span></p>
        <p><b>b</b><span><strong>Aprovar o PAF 2027</strong> pela regra C inteiro + B até o limite + sorteio do A, com os números da extração oficial de 30/09/2026.</span></p>
        <p><b>c</b><span><strong>Aprovar o sorteio do Grupo A</strong> (IPR-SORTEIO-V1), executado na extração oficial com as taxas vigentes, com publicação do compromisso e do resultado.</span></p>
        <p><b>d</b><span><strong>Tomar ciência</strong> de que GREBL, GREMN e URESN estão no limite: ampliar o Grupo B depende de lotação.</span></p>
      </div>
    </div>
    <div class="enc">
      <div class="enc-top" style="background:linear-gradient(135deg,#003366,#0066CC);"><i class="fas fa-layer-group"></i> Fiscalizações temáticas</div>
      <div class="enc-body">
        <p><b>1</b><span><strong>Dispensar a Tomada de Subsídios</strong> neste ciclo e institucionalizar a consulta externa nos próximos, com a SRG.</span></p>
        <p><b>2</b><span><strong>Manter quatro temáticas</strong> com escopo ajustado e renomear a de contêineres para <strong>Serviços em terminais de contêineres</strong>.</span></p>
        <p><b>3</b><span><strong>Substituir três</strong> e aprovar o recorte inicial de APs (5) e convênios (12).</span></p>
        <p><b>4</b><span><strong>Encaminhar</strong> duas matérias ao GEF Investimentos e articular com o GT do tema 2.8, MAPA, ANVISA e a área do IDA.</span></p>
        <p><b>5</b><span><strong>Escolher as três temáticas complementares</strong> após a consulta às URs, que se encerra hoje.</span></p>
      </div>
    </div>
  </div>
  <div class="px-16 pb-2">
    <div class="destaque flex items-center gap-6">
      <i class="fas fa-flag-checkered text-3xl" style="color:#FFD700;"></i>
      <p class="text-lg" style="margin:0;"><strong>Rito:</strong> elaboração pela GPF (RI, art. 80, III, &ldquo;a&rdquo;), consolidação e submissão pela SFC (art. 76, VIII)
      e aprovação pela Diretoria Colegiada (art. 11, X) — <strong style="color:#FFD700;">até 31/10/2026</strong>.</p>
    </div>
  </div>
  <p class="fonte px-16 pb-1">Fonte: {NTM}, item 12; {NT}, item 8.2.</p>
""",
    extra_css="""
.enc { border:1px solid #E2E8F0; border-radius:18px; overflow:hidden; display:flex; flex-direction:column; }
.enc-top { color:#fff; padding:14px 22px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(22px * var(--tz)); display:flex; gap:12px; align-items:center; }
.enc-body { flex:1; padding:14px 22px; display:flex; flex-direction:column; justify-content:space-evenly; gap:8px; }
.enc-body p { margin:0; display:flex; gap:14px; align-items:flex-start; }
.enc-body b {
  min-width:32px; height:32px; border-radius:50%; background:#F1F5F9; color:#003366;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(15px * var(--tz));
}
.enc-body span { color:#475569; font-size:calc(17px * var(--tz)); line-height:1.45; }
.enc-body strong { color:#003366; }
""",
    tag=TAG_GERAL,
    base=1.61,
)

SLIDES.append(dict(n=17, raw=True))

# Os slides acima levam o número em que foram escritos; a posição final no deck abre
# espaço para as duas divisórias de bloco (3 e 9). A capa (1) e o encerramento (19) são
# escritos à mão.
POSICAO = {2: 2, **{n: n + 1 for n in range(3, 8)}, **{n: n + 2 for n in range(8, 17)}}
for s in SLIDES:
    if not s.get("raw"):
        s["n"] = POSICAO[s["n"]]


# ---------------------------------------------------------------------------
# Divisórias de bloco — espelham IA-Dia-a-Dia-SFC/slide-04.html (KIT, seção 7.1)
# ---------------------------------------------------------------------------
DIVISOR = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>
body {{ margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }}
.slide {{ width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden;
  background:linear-gradient(135deg, #002244 0%, #003366 50%, #004488 100%); color:white; }}
.font-montserrat {{ font-family:'Montserrat',sans-serif; }}
.accent-left-gold {{ position:absolute; left:0; top:0; width:12px; height:100%; background:#FFD700; z-index:20; }}
.accent-left-blue {{ position:absolute; left:12px; top:0; width:4px; height:100%; background:#0066CC; z-index:20; }}
.shape-circle {{ position:absolute; border-radius:50%; z-index:0; }}
.shape-1 {{ width:620px; height:620px; top:-180px; right:-160px; border:60px solid rgba(255,255,255,0.03); }}
.shape-2 {{ width:420px; height:420px; bottom:-140px; right:18%; border:40px solid rgba(255,255,255,0.03); }}
.bg-pattern {{ background-image:radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px); background-size:22px 22px; }}
.module-num {{ font-family:'Montserrat',sans-serif; font-weight:900; line-height:0.9; font-size:188px;
  letter-spacing:-4px; color:#FFD700; text-shadow:0 8px 24px rgba(0,0,0,0.35); }}
.seal {{ display:inline-flex; align-items:center; gap:16px;
  background:linear-gradient(90deg, rgba(255,215,0,0.16) 0%, rgba(255,215,0,0.04) 100%);
  border:2px solid rgba(255,215,0,0.55); border-radius:999px; padding:16px 34px; }}
.chip {{ display:flex; align-items:center; gap:18px; background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.14); border-radius:16px; padding:22px 22px; }}
.chip-icon {{ width:64px; height:64px; border-radius:14px; flex-shrink:0; display:flex; align-items:center;
  justify-content:center; font-size:28px; background:rgba(0,102,204,0.30); color:#7CC0FF; }}
.chip-text {{ font-family:'Montserrat',sans-serif; font-weight:600; color:#FFFFFF; font-size:22px; line-height:1.25; margin:0; }}
</style>
</head>
<body>
<div class="slide">
  <div class="accent-left-gold"></div>
  <div class="accent-left-blue"></div>
  <div class="shape-circle shape-1"></div>
  <div class="shape-circle shape-2"></div>
  <div class="absolute inset-0 bg-pattern"></div>
  <img src="assets/logo-antaq-branca.png" alt="" class="absolute"
       style="top:42%; left:66%; width:48vw; max-width:720px; transform:translate(-50%,-50%); opacity:0.05; z-index:0; pointer-events:none;"/>
  <div class="absolute text-white z-0"
       style="bottom:-60px; right:-40px; font-size:500px; line-height:0; opacity:0.05; transform:translate(8%,8%);">
    <i class="fas {icone}"></i>
  </div>

  <div class="absolute z-10 flex items-center gap-4" style="top:56px; left:96px;">
    <img src="assets/logo-antaq-branca.png" alt="Logo ANTAQ" style="height:52px; width:auto;"/>
    <div style="border-left:1px solid rgba(255,255,255,0.20); padding-left:18px;">
      <p class="font-montserrat font-bold uppercase" style="font-size:18px; letter-spacing:.18em; color:#BFDBFE;">PAF 2027 · Apresentação ao Diretor-Geral</p>
      <p class="font-montserrat font-semibold uppercase" style="font-size:17px; letter-spacing:.12em; color:#93C5FD; opacity:.85;">SFC · GRAT · GPF · GCOR</p>
    </div>
  </div>

  <div class="relative z-10 flex-1 flex flex-col justify-center"
       style="padding-left:96px; padding-right:80px; padding-top:96px; padding-bottom:24px;">
    <div class="flex items-center gap-4" style="margin-bottom:26px;">
      <div style="width:72px; height:4px; background-color:#FFD700;"></div>
      <p class="font-montserrat font-semibold uppercase" style="font-size:22px; letter-spacing:.3em; color:#BFDBFE;">Bloco</p>
    </div>
    <div class="flex items-end" style="gap:40px; margin-bottom:46px;">
      <span class="module-num">{num}</span>
      <div style="border-left:5px solid rgba(255,215,0,0.55); padding-left:36px; padding-bottom:10px;">
        <h1 class="font-montserrat font-black text-white" style="font-size:80px; line-height:1.06; letter-spacing:-1.5px;">{titulo}</h1>
        <p class="font-montserrat" style="font-size:30px; font-weight:400; line-height:1.4; color:#DBEAFE; max-width:1300px; margin-top:16px;">{resumo}</p>
      </div>
    </div>
    <div class="grid grid-cols-{ncol}" style="gap:20px; max-width:1640px;">
{chips}
    </div>
    <div style="margin-top:44px;">
      <span class="seal">
        <i class="fas fa-file-lines" style="color:#FFD700; font-size:28px;"></i>
        <span class="font-montserrat" style="font-size:26px; font-weight:700; color:#fff;">{base_doc}</span>
      </span>
    </div>
  </div>

  <div class="relative z-10 flex justify-between items-end" style="padding:0 96px 32px;">
    <p class="font-montserrat" style="font-size:18px; color:#BFDBFE; opacity:.75;">{rodape}</p>
    <p class="font-mono" style="font-size:18px; color:#BFDBFE; opacity:.75;">{n} / {total}</p>
  </div>
</div>
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""


def divisor(n, num, titulo, resumo, icone, chips, base_doc):
    html_chips = "\n".join(
        f'      <div class="chip"><div class="chip-icon"><i class="fas {ic}"></i></div>'
        f'<p class="chip-text">{tx}</p></div>'
        for ic, tx in chips
    )
    (DST / f"slide-{n:02d}.html").write_text(DIVISOR.format(
        title=f"Bloco {int(num)} — {titulo}", num=num, titulo=titulo, resumo=resumo,
        icone=icone, chips=html_chips, ncol=len(chips), base_doc=base_doc,
        rodape=RODAPE, n=n, total=TOTAL,
    ), encoding="utf-8")
    print(f"slide-{n:02d}.html (divisória)")


divisor(
    3, "01", "Fiscalizações do grupo de risco",
    "Quem fiscalizar, e com que intensidade: a nota de risco de cada outorga define a ação, "
    "e o plano precisa caber na equipe e no orçamento.",
    "fa-gauge-high",
    [("fa-stairs", "Do risco à ação fiscal"), ("fa-eye", "IPR 2.0: o que mudou"),
     ("fa-list-check", "O que entra no PAF 2027"), ("fa-users", "Força de trabalho"),
     ("fa-plane", "Custo de deslocamento")],
    "Minuta da NT de Metodologia do PAF 2027 · IPR 2.0",
)
divisor(
    9, "02", "Fiscalizações temáticas",
    "Que problema do setor examinar a fundo: das 99 contribuições da revisão da Agenda "
    "Regulatória às sete temáticas de 2027.",
    "fa-layer-group",
    [("fa-inbox", "99 demandas externas"), ("fa-check-double", "O que já está coberto"),
     ("fa-arrows-rotate", "Manter quatro, substituir três"), ("fa-building-columns", "APs e convênios"),
     ("fa-list-ol", "Candidatos às três vagas")],
    "Nota Técnica nº 27/2026/GPF/SFC · SEI 3024667",
)


def render(s):
    css = f':root {{ --tz-base: {s.get("base", 1.0) * TEXT_SCALE:.4g}; }}\n' + BASE_CSS + s.get("extra_css", "")
    return HEAD.format(
        title=s["title"], css=css, kicker=s["kicker"], titulo=s["titulo"],
        tag=s.get("tag", ""), body=s["body"], rodape=RODAPE, n=s["n"], total=TOTAL,
    )


for s in sorted(SLIDES, key=lambda s: s["n"]):
    if s.get("raw"):
        continue
    (DST / f"slide-{s['n']:02d}.html").write_text(render(s), encoding="utf-8")
    print(f"slide-{s['n']:02d}.html")
