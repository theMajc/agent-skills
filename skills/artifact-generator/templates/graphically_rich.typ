#let data_file = sys.inputs.at("data_file")
#let cv = json(data_file)

#let primary-color = rgb("#4338ca") // Indigo-700
#let secondary-color = rgb("#0284c7") // Sky-600
#let card-bg = rgb("#f8fafc")
#let border-color = rgb("#e2e8f0")

#set page(
  paper: "a4",
  margin: (x: 1.6cm, top: 1.6cm, bottom: 1.6cm),
  footer: context [
    #align(center)[
      #text(size: 8pt, fill: rgb("#94a3b8"), font: "DejaVu Sans")[
        *#cv.basics.name* #sym.bullet High-Fidelity Profile Dossier #sym.bullet Page #counter(page).display("1 of 1", both: true)
      ]
    ]
  ]
)

#set text(
  font: "DejaVu Sans",
  size: 9.5pt,
  fill: rgb("#1e293b"),
  lang: "en"
)

// Hero Banner
#rect(
  fill: rgb("#0f172a"),
  radius: 6pt,
  width: 100%,
  inset: (x: 16pt, y: 14pt)
)[
  #grid(
    columns: (1fr, auto),
    [
      #text(size: 20pt, weight: "bold", fill: white)[#cv.basics.name] \
      #v(3pt)
      #text(size: 11pt, weight: "medium", fill: rgb("#93c5fd"))[#cv.basics.label]
    ],
    [
      #align(right + top)[
        #text(size: 8.5pt, fill: rgb("#cbd5e1"))[
          #cv.basics.location.city, #cv.basics.location.region \
          #link("mailto:" + cv.basics.email)[#text(fill: rgb("#38bdf8"))[#cv.basics.email]] \
          #cv.basics.phone \
          #link(cv.basics.url)[#text(fill: rgb("#38bdf8"))[#cv.basics.url]]
        ]
      ]
    ]
  )
]

#v(8pt)

// Metric Callouts
#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 10pt,
  rect(
    fill: rgb("#eef2ff"),
    stroke: 1pt + rgb("#c7d2fe"),
    radius: 4pt,
    inset: 8pt,
    align(center)[
      #text(size: 14pt, weight: "bold", fill: primary-color)[-84%]\
      #text(size: 7.5pt, weight: "bold", fill: rgb("#475569"))[P99 TASK LATENCY]
    ]
  ),
  rect(
    fill: rgb("#f0fdf4"),
    stroke: 1pt + rgb("#bbf7d0"),
    radius: 4pt,
    inset: 8pt,
    align(center)[
      #text(size: 14pt, weight: "bold", fill: rgb("#15803d"))[4.2M / s]\
      #text(size: 7.5pt, weight: "bold", fill: rgb("#475569"))[EDGE INGRESS THROUGHPUT]
    ]
  ),
  rect(
    fill: rgb("#f0f9ff"),
    stroke: 1pt + rgb("#bae6fd"),
    radius: 4pt,
    inset: 8pt,
    align(center)[
      #text(size: 14pt, weight: "bold", fill: secondary-color)[18 GB/s]\
      #text(size: 7.5pt, weight: "bold", fill: rgb("#475569"))[ZERO-COPY STORAGE IO]
    ]
  )
)

#v(4pt)

// Section Macro
#let section(title, icon_char: "■") = [
  #v(8pt)
  #grid(
    columns: (auto, 1fr),
    gutter: 6pt,
    text(fill: primary-color, size: 10pt)[#icon_char],
    [
      #text(size: 11pt, weight: "bold", fill: rgb("#0f172a"))[#title]
      #v(-4pt)
      #line(length: 100%, stroke: 0.8pt + rgb("#cbd5e1"))
    ]
  )
  #v(3pt)
]

// Summary Box
#section("Executive Overview")
#rect(
  fill: card-bg,
  stroke: 0.8pt + border-color,
  radius: 4pt,
  inset: 10pt,
  width: 100%
)[
  #text(style: "italic", size: 9pt, fill: rgb("#334155"))[#cv.basics.summary]
]

// Experience
#section("Professional Trajectory")
#for job in cv.work [
  #rect(
    fill: white,
    stroke: 0.8pt + border-color,
    radius: 4pt,
    inset: 10pt,
    width: 100%
  )[
    #grid(
      columns: (1fr, auto),
      [
        #text(weight: "bold", size: 10.5pt, fill: primary-color)[#job.position] \
        #text(weight: "semibold", size: 9pt, fill: rgb("#475569"))[#job.name]
      ],
      [
        #align(right)[
          #rect(
            fill: rgb("#f1f5f9"),
            radius: 3pt,
            inset: (x: 6pt, y: 3pt)
          )[
            #text(size: 8pt, weight: "bold", fill: rgb("#475569"))[#job.startDate #sym.dash.en #job.endDate]
          ]
        ]
      ]
    )
    #v(3pt)
    #text(size: 9pt)[#job.summary]
    #v(3pt)
    #list(
      marker: text(fill: secondary-color)[▶],
      ..job.highlights.map(h => text(size: 8.8pt)[#h])
    )
  ]
  #v(4pt)
]

// Skills with Badges
#section("Technical Arsenal")
#for skill in cv.skills [
  #text(weight: "bold", size: 9pt)[#skill.name:]
  #h(4pt)
  #box[
    #for kw in skill.keywords [
      #box(
        fill: rgb("#ede9fe"),
        outset: 2pt,
        radius: 3pt,
        inset: (x: 4pt, y: 1pt),
        baseline: 0%
      )[#text(size: 8pt, weight: "medium", fill: rgb("#5b21b6"))[#kw]]
      #h(3pt)
    ]
  ]
  #v(2pt)
]

// Education & Creds
#section("Education & Credentials")
#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  rect(
    fill: card-bg,
    stroke: 0.8pt + border-color,
    radius: 4pt,
    inset: 8pt,
    [
      #for edu in cv.education [
        #text(weight: "bold", size: 9pt)[#edu.institution] \
        #text(size: 8.5pt)[#edu.studyType in #edu.area] \
        #text(size: 8pt, fill: rgb("#64748b"))[GPA: #edu.score | #edu.startDate #sym.dash.en #edu.endDate]
      ]
    ]
  ),
  rect(
    fill: card-bg,
    stroke: 0.8pt + border-color,
    radius: 4pt,
    inset: 8pt,
    [
      #if "certifications" in cv and cv.certifications.len() > 0 [
        #for cert in cv.certifications [
          #text(weight: "bold", size: 9pt)[#cert.name] \
          #text(size: 8.5pt, fill: rgb("#475569"))[#cert.issuer (#cert.date)]
        ]
      ]
    ]
  )
)
