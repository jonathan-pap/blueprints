Design Brief:
  generated_by: powerbi-report-design-room
  contract_version: 1
  mode: greenfield
  request: "4 pages for an executive sales review — pages that tell a story"
  data_source: test.SemanticModel (Financial Sample)
  design_identity:
    tone: >
      Editorial Newsroom — reads like a Sunday business broadsheet. Cream surface,
      serif display headlines (Georgia), Segoe UI body, ONE sharp accent (mustard),
      no chart gridlines, hairline rules between sections. Domain default for
      board/finance review; built for narrative. (Surfaced ASSUMPTION — prompt was
      tone-silent; finance+executive+"tells a story" -> Editorial Newsroom.)
    signature: >
      S2 display serif headlines (each page opens with a Georgia insight headline)
      + S1 tabular numerals throughout (values column-align). Coherent pair per
      signatures matrix.
  color_map:
    - measure: '_Measures'[Total Sales]   # hero accent
      color: "#D4A30A"
      tint:  "#F7EAC4"
    - measure: '_Measures'[Total Profit]  # serious second measure = ink
      color: "#0F172A"
      tint:  "#E2E5EA"
    - measure: '_Measures'[Profit %]
      color: "#1C5E47"                     # forest = the rate
      tint:  "#D7E5DF"
    # variance polarity — status, not decoration (matches model Delta Color)
    - variance_up:   "#1B7F4A"
    - variance_down: "#B00020"

  # ---- THE STORY ARC: 4 distinct archetypes (no mono-archetype) ----
  # Stand -> Story -> Drivers -> Verdict
  pages:

    - name: "Where We Stand: Sales, Profit & Target"   # finalize w/ number after DAX read
      role: landing
      archetype: Executive Summary
      layout_variant: "KPI strip + dual hero"
      variant_rationale: "3-4 co-equal headline KPIs + a clear trend + one driver -> strip over dual hero."
      page_size: { width: 1280, height: 720 }
      page_background: "#FAF7F0"
      layout_contract:
        header_band:
          - { id: page_title, kind: textbox, text: "Where We Stand", purpose: "Open with the verdict." }
          - { id: year_slicer, kind: slicer, field_bindings: financials[Year], slicer_type: dropdown }
        zone1_summary:
          token: layouts.kpi_row_4
          placements:
            - { id: c_sales,  kind: cardVisual, field_bindings: '_Measures'[Total Sales],  context: '_Measures'[Sales PY], color_strategy: measure_match, purpose: "Total sales vs last year?" }
            - { id: c_profit, kind: cardVisual, field_bindings: '_Measures'[Total Profit], context: '_Measures'[Profit %],  color_strategy: measure_match, purpose: "Profit and its margin?" }
            - { id: c_units,  kind: cardVisual, field_bindings: '_Measures'[Total Units],  purpose: "Volume sold?" }
            - { id: c_asp,    kind: cardVisual, field_bindings: '_Measures'[Avg Sale Price], purpose: "Average price point?" }
        zone2_analysis:
          placements:
            - { id: trend, kind: lineChart, field_bindings: { axis: financials[Month Name], values: ['_Measures'[Total Sales], '_Measures'[Sales PY]] }, color_strategy: measure_match, purpose: "How is sales trending vs PY?" }
            - { id: by_segment, kind: barChart, field_bindings: { category: financials[Segment], values: '_Measures'[Total Sales] }, sort_policy: value_desc, color_strategy: gradient, purpose: "Which segment drives sales?" }
        zone3_detail:
          placements:
            - { id: country_tbl, kind: tableEx, field_bindings: [financials[Country], '_Measures'[Total Sales], '_Measures'[Profit %]], purpose: "Sales + margin by country." }
      space_budget: { zones_used: [header_band, zone1_summary, zone2_analysis, zone3_detail], empty_zones: [], largest_zone: zone2_analysis }

    - name: "The Year in Months: When We Beat Target"
      role: detail
      archetype: Narrative Story
      layout_variant: "Headline + evidence + takeaway"
      variant_rationale: "Model ships TAKEAWAY + streak/best-month measures -> author-driven argument, not exploration."
      page_size: { width: 1280, height: 720 }
      page_background: "#FAF7F0"
      layout_contract:
        header_band:
          - { id: page_title, kind: textbox, text: "The Year in Months", purpose: "Frame the narrative." }
        zone1_summary:
          token: layouts.kpi_row_3
          placements:
            - { id: c_wins,   kind: cardVisual, field_bindings: '_Measures'[Number Successful Months], context: "months beaten vs 12", purpose: "How many months beat target?" }
            - { id: c_best,   kind: cardVisual, field_bindings: '_Measures'[Best Month], purpose: "Strongest month?" }
            - { id: c_streak, kind: cardVisual, field_bindings: '_Measures'[Longest Winning Streak], purpose: "Longest run of wins?" }
        zone2_analysis:
          placements:
            - { id: avt_columns, kind: clusteredColumnChart, field_bindings: { axis: financials[Month Name], values: ['_Measures'[GREEN MAX], '_Measures'[RED MAX]], line: '_Measures'[Sales Target] }, color_strategy: "variance polarity (green beat / red miss)", purpose: "Which months beat vs missed target?" }
        zone3_detail:
          placements:
            - { id: takeaway, kind: textbox, field_bindings: '_Measures'[TAKEAWAY], purpose: "The narrative payoff sentence — generated by the model." }
      space_budget: { zones_used: [header_band, zone1_summary, zone2_analysis, zone3_detail], empty_zones: [], largest_zone: zone2_analysis }

    - name: "What's Driving Sales"
      role: detail
      archetype: Analytical Canvas
      layout_variant: "Filter-Rail"
      variant_rationale: "3 categorical dims (Segment/Country/Product) + hypothesis testing -> left filter rail + multi-chart canvas."
      page_size: { width: 1280, height: 720 }
      page_background: "#FAF7F0"
      layout_contract:
        header_band:
          - { id: page_title, kind: textbox, text: "What's Driving Sales", purpose: "Name the question." }
        filter_rail:
          - { id: s_segment, kind: slicer, field_bindings: financials[Segment] }
          - { id: s_country, kind: slicer, field_bindings: financials[Country] }
        zone2_analysis:
          placements:
            - { id: pareto, kind: lineClusteredColumnComboChart, field_bindings: { axis: financials[Product], columns: '_Measures'[Total Sales], line: '_Measures'[Cumulative %] }, sort_policy: value_desc, color_strategy: "Pareto Bar Color", purpose: "Which few products make most sales?" }
            - { id: c_to80, kind: cardVisual, field_bindings: '_Measures'[# Products to 80%], purpose: "How many products = 80% of sales?" }
            - { id: scatter, kind: scatterChart, field_bindings: { x: '_Measures'[Total Sales], y: '_Measures'[Profit %], details: financials[Product] }, purpose: "Sales vs margin by product — find low-margin volume." }
        zone3_detail:
          placements:
            - { id: seg_year, kind: clusteredColumnChart, field_bindings: { axis: financials[Segment], legend: financials[Year], values: '_Measures'[Total Sales] }, purpose: "Segment sales by year." }
      space_budget: { zones_used: [header_band, filter_rail, zone2_analysis, zone3_detail], empty_zones: [], largest_zone: zone2_analysis }

    - name: "Winners & Laggards vs Target"
      role: detail
      archetype: Comparative Benchmark
      layout_variant: "Ranked bars + variance table"
      variant_rationale: "Ranking/benchmark question + model ships IBCS/bullet variance SVGs -> ranked bars + SVG variance table."
      page_size: { width: 1280, height: 720 }
      page_background: "#FAF7F0"
      layout_contract:
        header_band:
          - { id: page_title, kind: textbox, text: "Winners & Laggards", purpose: "State the comparison." }
        zone2_analysis:
          placements:
            - { id: country_rank, kind: barChart, field_bindings: { category: financials[Country], values: '_Measures'[Total Sales] }, sort_policy: value_desc, color_strategy: gradient, purpose: "Top/bottom countries by sales." }
            - { id: seg_margin, kind: barChart, field_bindings: { category: financials[Segment], values: '_Measures'[Profit %] }, sort_policy: value_desc, color_strategy: gradient, purpose: "Margin ranking by segment." }
        zone3_detail:
          placements:
            - { id: variance_tbl, kind: tableEx, field_bindings: [financials[Product], '_Measures'[Total Sales], '_Measures'[% Delta], '_Measures'[Sales IBCS Bar SVG]], sort_policy: "% Delta asc (worst first)", purpose: "Per-product actual-vs-target with inline IBCS variance bar." }
      space_budget: { zones_used: [header_band, zone2_analysis, zone3_detail], empty_zones: [], largest_zone: zone3_detail }

  interaction_pattern:
    nav: "Bookmark/button navigator across the 4 pages (consistent placement)."
    cross_filter_rules: "Filter (default); ranked bars on p4 -> Highlight."
  accessibility:
    alt_text: "every chart gets a headline+trend alt string"
    contrast: "WCAG AA on cream surface; variance red/green carries a non-color cue (label/sign)"
  theme:
    base: "New Editorial Newsroom theme (cream #FAF7F0, Georgia display via textClasses, Segoe body, mustard accent, no gridlines, hairline section rules). Preserve per-type safeguards (textbox/card zero padding, table grow-to-fit, hidden headers)."

# Build notes (authoring handoff):
#  - pages.json already pinned to pagesMetadata/1.0.0 -> pbir add page WILL write (no schema-lag block).
#  - reference pages by DISPLAY NAME; keep names unique; verify with `pbir ls`; visuals at y>=120.
#  - finalize the number-bearing insight titles on p1/p2 after a DAX read of the real totals.
#  - long visual types (lineClusteredColumnComboChart) need explicit --name to avoid schema length limit.
