#let data_file = sys.inputs.at("data_file")
#let cv = json(data_file)

#set page(
  paper: "a4",
  margin: (x: 1.8cm, top: 1.8cm, bottom: 1.8cm),
  footer: context [
    #align(center)[
      #text(size: 8.5pt, fill: rgb("#666666"), font: "Libertinus Serif")[
        #cv.basics.name #sym.dash.en Page #counter(page).display("1 of 1", both: true)
      ]
    ]
  ]
)

#set text(
  font: "Libertinus Serif",
  size: 10pt,
  fill: rgb("#1a1a1a"),
  lang: "en"
)

#set par(justify: true, leading: 0.65em)

// Header Block
#align(center)[
  #text(size: 20pt, weight: "bold", tracking: 0.5pt)[#cv.basics.name] \
  #v(2pt)
  #text(size: 11pt, style: "italic", fill: rgb("#333333"))[#cv.basics.label] \
  #v(4pt)
  #text(size: 9pt, fill: rgb("#555555"))[
    #cv.basics.location.city, #cv.basics.location.region #sym.bullet
    #link("mailto:" + cv.basics.email)[#cv.basics.email] #sym.bullet
    #cv.basics.phone #sym.bullet
    #link(cv.basics.url)[#cv.basics.url]
  ]
]

#v(6pt)

// Section Macro
#let section(title) = {
  v(8pt)
  text(size: 11pt, weight: "bold", tracking: 1pt)[#upper(title)]
  v(-3pt)
  line(length: 100%, stroke: 0.5pt + rgb("#888888"))
  v(2pt)
}

// Executive Summary
#section("Executive Summary")
#cv.basics.summary

// Professional Experience
#section("Professional Experience")
#for job in cv.work [
  #grid(
    columns: (1fr, auto),
    [
      #text(weight: "bold", size: 10.5pt)[#job.position] \
      #text(style: "italic", fill: rgb("#2b2b2b"))[#job.name]
    ],
    [
      #align(right)[
        #text(size: 9pt, fill: rgb("#555555"))[#job.startDate #sym.dash.en #job.endDate] \
        #text(size: 8.5pt, fill: rgb("#777777"))[#cv.basics.location.city, #cv.basics.location.region]
      ]
    ]
  )
  #v(2pt)
  #job.summary
  #v(2pt)
  #list(
    ..job.highlights.map(h => text(size: 9.5pt)[#h])
  )
  #v(4pt)
]

// Technical Core Competencies
#section("Core Competencies & Technical Mastery")
#for skill in cv.skills [
  *#skill.name:* #skill.keywords.join(", ") \
  #v(1pt)
]

// Key Projects
#if "projects" in cv and cv.projects.len() > 0 [
  #section("Key Architecture Projects")
  #for proj in cv.projects [
    #grid(
      columns: (1fr, auto),
      [
        #text(weight: "bold")[#proj.name] #if "url" in proj [ #sym.bullet #link(proj.url)[#text(size: 8.5pt)[#proj.url]] ]
      ],
      []
    )
    #proj.description
    #list(
      ..proj.highlights.map(h => text(size: 9.5pt)[#h])
    )
  ]
]

// Education
#section("Education & Credentials")
#for edu in cv.education [
  #grid(
    columns: (1fr, auto),
    [
      #text(weight: "bold")[#edu.institution] \
      #text(style: "italic")[#edu.studyType in #edu.area]
    ],
    [
      #align(right)[
        #text(size: 9pt, fill: rgb("#555555"))[#edu.startDate #sym.dash.en #edu.endDate] \
        #text(size: 8.5pt, fill: rgb("#444444"))[GPA: #edu.score]
      ]
    ]
  )
]

// Certifications
#if "certifications" in cv and cv.certifications.len() > 0 [
  #for cert in cv.certifications [
    #v(2pt)
    #text(weight: "bold")[#cert.name] #sym.dash.en #cert.issuer (#cert.date)
  ]
]
