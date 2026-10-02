# PAF 2027 — Apresentação ao Diretor-Geral (02/10/2026)

Deck de 19 slides (capa, visão geral, dois blocos com divisória própria, fiscalizações operacionais, síntese e encerramento), no mesmo template do deck
`EncontroChefias2026/apresentacao_ipr_paf2027/`.

- `slide-01.html` (capa) e `slide-19.html` (encerramento): escritos à mão, fundo escuro.
- `slide-02.html`..`slide-18.html`: gerados por `build_slides.py` (`python3 build_slides.py`).
  - 02 visão geral e calendário
  - 03 divisória e 04–08 Bloco 1, fiscalizações do grupo de risco (IPR 2.0)
  - 09 divisória e 10–16 Bloco 2, fiscalizações temáticas (NT nº 27/2026/GPF/SFC)
  - 17 fiscalizações operacionais (adaptado de `../operacionais-paf2027-dg.pptx`)
  - 18 síntese e encaminhamentos
  - As divisórias seguem `IA-Dia-a-Dia-SFC/slide-04.html`. No gerador, cada slide leva o número
    em que foi escrito e o dicionário `POSICAO` dá a posição final no deck.
- Fontes dos números: minuta da NT de Metodologia do PAF 2027 (rodada de validação de 29/09/2026,
  `/home/pedro/IPR-PAF/docs/notas-tecnicas/NT_Metodologia_PAF_2027.html`), banco do painel IPR-PAF
  (ICF, em 01/10/2026) e a NT 27/2026 (SEI 3024667) com a apresentação `PAF2027_NT27_Apresentacao_DG.pptx`.
- O `base=` de cada slide foi fechado em 95% do maior fator de texto que cabe sem invadir o rodapé
  (medido no Chrome). Depois de mexer no conteúdo, remedir antes de subir o `base`.

Para ver: `python3 -m http.server 8765` nesta pasta e abrir `http://localhost:8765/`.
