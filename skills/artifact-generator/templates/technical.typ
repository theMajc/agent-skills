#let data_file = sys.inputs.at("data_file")
#let cv = json(data_file)

#set page(
  paper: "a4",
  margin: (x: 1.4cm, top: 1.4cm, bottom: 1.4cm),
  footer: context [
    #grid(
      columns: (1fr, 1fr),
      [
        #text(size: 8pt, fill: rgb("#666666"), font: "DejaVu Sans")[
          *#cv.basics.name* | Systems Architecture & Runtimes Dossier
        ]
      ],
      [
        #align(right)[
          #text(size: 8pt, fill: rgb("#666666"), font: "DejaVu Sans Mono")[
            [#counter(page).display("1 of 1", both: true)]
          ]
        ]
      ]
    )
  ]
)

#set text(
  font: "DejaVu Sans",
  size: 9pt,
  fill: rgb("#111827"),
  lang: "en"
)

#set par(justify: true, leading: 0.55em)

// Technical Header
#grid(
  columns: (3fr, 2fr),
  [
    #text(size: 18pt, weight: "bold", fill: rgb("#0f172a"))[#cv.basics.name] \
    #v(2pt)
    #text(size: 10pt, weight: "medium", fill: rgb("#2563eb"))[#cv.basics.label]
  ],
  [
    #align(right)[
      #text(size: 8.5pt, font: "DejaVu Sans Mono", fill: rgb("#475569"))[
        #link("mailto:" + cv.basics.email)[#cv.basics.email] \
        #cv.basics.phone \
        #link(cv.basics.url)[#cv.basics.url] \
        #cv.basics.location.city, #cv.basics.location.region
      ]
    ]
  ]
)

#v(4pt)
#line(length: 100%, stroke: 1.5pt + rgb("#2563eb"))
#v(4pt)

// Dense Section Macro
#let section(title) = {
  v(6pt)
  rect(
    fill: rgb("#f1f5f9"),
    inset: (x: 6pt, y: 3pt),
    radius: 2pt,
    width: 100%
  )[
    #text(size: 9.5pt, weight: "bold", fill: rgb("#1e293b"))[#upper(title)]
  ]
  v(2pt)
}

// Executive / Systems Summary
#section("Architectural Profile")
#cv.basics.summary

// Skills Matrix
#section("Technical Competencies & Systems Matrix")
#table(
  columns: (1fr, 3fr),
  stroke: (x, y) => if y == 0 { (bottom: 0.5pt + rgb("#cbd5e1")) } else { (bottom: 0.2pt + rgb("#e2e8f0")) },
  fill: (col, row) => if calc.odd(row) { rgb("#f8fafc") } else { none },
  inset: (x: 5pt, y: 4pt),
  ..cv.skills.map(s => (
    text(weight: "bold", size: 8.5pt)[#s.name],
    text(size: 8.5pt, font: "DejaVu Sans Mono")[#s.keywords.join("  |  ")]
  )).flatten()
)

// Experience with Metrics Callouts
#section("Engineering Leadership & Production Impact")
#for job in cv.work [
  #grid(
    columns: (1fr, auto),
    [
      #text(weight: "bold", size: 9.5pt, fill: rgb("#0f172a"))[#job.position] #sym.dash.en #text(weight: "semibold", fill: rgb("#334155"))[#job.name]
    ],
    [
      #align(right)[
        #text(size: 8.5pt, font: "DejaVu Sans Mono", fill: rgb("#64748b"))[#job.startDate #sym.dash.en #job.endDate]
      ]
    ]
  )
  #v(1pt)
  #text(size: 8.5pt, style: "italic", fill: rgb("#334155"))[#job.summary]
  #v(1pt)
  #list(
    marker: [•],
    ..job.highlights.map(h => text(size: 8.5pt)[#h])
  )
  #v(2pt)
]

// Projects & Infrastructure OSS
#if "projects" in cv and cv.projects.len() > 0 [
  #section("Mission-Critical Open Source & Tooling")
  #for proj in cv.projects [
    #grid(
      columns: (1fr, auto),
      [
        #text(weight: "bold", size: 9pt)[#proj.name] #if "url" in proj [ #sym.bullet #link(proj.url)[#text(size: 8pt, font: "DejaVu Sans Mono")[#proj.url]] ]
      ],
      []
    )
    #text(size: 8.5pt)[#proj.description]
    #list(
      marker: [•],
      ..proj.highlights.map(h => text(size: 8.5pt)[#h])
    )
  ]
]

// Education & Certifications
#section("Education & Credentials")
#grid(
  columns: (3fr, 2fr),
  [
    #for edu in cv.education [
      #text(weight: "bold")[#edu.institution] \
      #text(size: 8.5pt)[#edu.studyType in #edu.area] (GPA: #edu.score) \
      #text(size: 8pt, fill: rgb("#64748b"))[#edu.startDate #sym.dash.en #edu.endDate]
    ]
  ],
  [
    #if "certifications" in cv and cv.certifications.len() > 0 [
      #for cert in cv.certifications [
        #text(weight: "bold")[#cert.name] \
        #text(size: 8.5pt, fill: rgb("#475569"))[#cert.issuer (#cert.date)]
      ]
    ]
  ]
)
