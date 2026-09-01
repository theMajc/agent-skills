#!/usr/bin/env python3
"""
Multica Dynamic Artifact Generator CLI
Orchestrates high-fidelity PDF, SVG, and standalone responsive HTML artifact generation.
"""

import argparse
import os
import sys
import subprocess
import time
import json

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def ensure_typst_binary():
    # 1. System PATH
    res = subprocess.run(["which", "typst"], capture_output=True, text=True)
    if res.returncode == 0:
        return res.stdout.strip()

    # 2. Local skill bin
    script_dir = get_script_dir()
    local_bin = os.path.abspath(os.path.join(script_dir, "../bin/typst"))
    if os.path.exists(local_bin) and os.access(local_bin, os.X_OK):
        return local_bin

    # 3. Scratch bin
    scratch_bin = os.path.abspath("scratch/bin/typst")
    if os.path.exists(scratch_bin) and os.access(scratch_bin, os.X_OK):
        return scratch_bin

    # Run ensure_typst.sh
    ensure_sh = os.path.join(script_dir, "ensure_typst.sh")
    if os.path.exists(ensure_sh):
        print("[artifact-generator] Bootstrapping standalone Typst binary...", file=sys.stderr)
        sub_res = subprocess.run(["bash", ensure_sh], capture_output=True, text=True)
        if sub_res.returncode == 0 and os.path.exists(local_bin):
            return local_bin

    raise RuntimeError("Typst binary could not be found or bootstrapped.")

def generate_interactive_html(json_path, output_path, preset="executive"):
    with open(json_path, 'r', encoding='utf-8') as f:
        cv = json.load(f)

    basics = cv.get("basics", {})
    work = cv.get("work", [])
    skills = cv.get("skills", [])
    projects = cv.get("projects", [])
    education = cv.get("education", [])
    certs = cv.get("certifications", [])

    theme_accent = "#4f46e5" if preset == "graphically_rich" else ("#2563eb" if preset == "technical" else "#334155")

    html = f"""<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{basics.get("name", "Artifact")} | {basics.get("label", "Profile")}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#eef2ff',
              100: '#e0e7ff',
              500: '{theme_accent}',
              600: '{theme_accent}',
              700: '{theme_accent}',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: white !important; color: black !important; font-size: 10pt; }}
      .card-shadow {{ box-shadow: none !important; border: 1px solid #e2e8f0; }}
      @page {{ margin: 1.5cm; }}
    }}
  </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors duration-200 antialiased min-h-screen py-8 px-4 sm:px-6 lg:px-8">
  <div class="max-w-4xl mx-auto space-y-6">
    
    <!-- Top Action Bar (No Print) -->
    <header class="no-print flex items-center justify-between bg-white dark:bg-slate-900 px-6 py-3 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
      <div class="flex items-center space-x-2">
        <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Interactive Web Presentation &bull; Preset: {preset.upper()}</span>
      </div>
      <div class="flex items-center space-x-3">
        <button id="theme-toggle" class="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition" title="Toggle Dark/Light Mode">
          🌓
        </button>
        <button onclick="window.print()" class="px-4 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:opacity-90 shadow-sm transition">
          Print / PDF
        </button>
      </div>
    </header>

    <!-- Hero Card -->
    <section class="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800 relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <h1 class="text-3xl sm:text-4xl font-black tracking-tight text-slate-900 dark:text-white">{basics.get("name")}</h1>
          <p class="text-lg font-medium text-blue-600 dark:text-blue-400 mt-1">{basics.get("label")}</p>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-2 flex flex-wrap gap-y-1 gap-x-4">
            <span>📍 {basics.get("location", {}).get("city")}, {basics.get("location", {}).get("region")}</span>
            <span>✉️ <a href="mailto:{basics.get("email")}" class="hover:underline">{basics.get("email")}</a></span>
            <span>📞 {basics.get("phone")}</span>
            <span>🌐 <a href="{basics.get("url")}" target="_blank" class="hover:underline">{basics.get("url")}</a></span>
          </p>
        </div>
      </div>
      <div class="mt-6 pt-6 border-t border-slate-100 dark:border-slate-800 text-slate-600 dark:text-slate-300 leading-relaxed text-sm">
        {basics.get("summary")}
      </div>
    </section>

    <!-- Skills Matrix -->
    <section class="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800">
      <h2 class="text-lg font-bold tracking-tight text-slate-900 dark:text-white uppercase mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-blue-600"></span> Core Competencies
      </h2>
      <div class="space-y-4">
    """

    for s in skills:
        html += f"""
        <div>
          <div class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">{s.get("name")}</div>
          <div class="flex flex-wrap gap-2">
        """
        for kw in s.get("keywords", []):
            html += f"""<span class="px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-xs font-medium border border-slate-200 dark:border-slate-700">{kw}</span>"""
        html += """
          </div>
        </div>
        """

    html += """
      </div>
    </section>

    <!-- Experience Timeline -->
    <section class="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800">
      <h2 class="text-lg font-bold tracking-tight text-slate-900 dark:text-white uppercase mb-6 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-blue-600"></span> Experience & Impact
      </h2>
      <div class="space-y-8">
    """

    for job in work:
        html += f"""
        <div class="border-l-2 border-blue-500 pl-4 sm:pl-6 space-y-2 relative">
          <div class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-blue-600 border-4 border-white dark:border-slate-900"></div>
          <div class="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1">
            <h3 class="text-base font-bold text-slate-900 dark:text-white">{job.get("position")}</h3>
            <span class="text-xs font-mono text-slate-500 dark:text-slate-400">{job.get("startDate")} &ndash; {job.get("endDate")}</span>
          </div>
          <div class="text-sm font-medium text-blue-600 dark:text-blue-400">{job.get("name")}</div>
          <p class="text-sm text-slate-600 dark:text-slate-300">{job.get("summary")}</p>
          <ul class="list-disc list-outside ml-4 text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-1 pt-1">
        """
        for hl in job.get("highlights", []):
            html += f"<li>{hl}</li>"
        html += """
          </ul>
        </div>
        """

    html += """
      </div>
    </section>

    <!-- Projects & Open Source -->
    <section class="bg-white dark:bg-slate-900 rounded-2xl p-8 shadow-sm border border-slate-200 dark:border-slate-800">
      <h2 class="text-lg font-bold tracking-tight text-slate-900 dark:text-white uppercase mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-blue-600"></span> Open Source & Architecture
      </h2>
      <div class="space-y-4">
    """

    for p in projects:
        html += f"""
        <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
          <div class="flex items-center justify-between">
            <div class="font-bold text-slate-900 dark:text-white text-sm">{p.get("name")}</div>
            <a href="{p.get("url", "#")}" target="_blank" class="text-xs font-mono text-blue-600 dark:text-blue-400 hover:underline">Repository &rarr;</a>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-300 mt-1">{p.get("description")}</p>
        </div>
        """

    html += f"""
      </div>
    </section>

    <!-- Education & Certifications -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <section class="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
        <h2 class="text-base font-bold text-slate-900 dark:text-white uppercase mb-3 flex items-center gap-2">
          🎓 Education
        </h2>
    """

    for edu in education:
        html += f"""
        <div class="text-sm">
          <div class="font-bold text-slate-900 dark:text-white">{edu.get("institution")}</div>
          <div class="text-blue-600 dark:text-blue-400 text-xs">{edu.get("studyType")} in {edu.get("area")}</div>
          <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">GPA: {edu.get("score")} &bull; {edu.get("startDate")} &ndash; {edu.get("endDate")}</div>
        </div>
        """

    html += f"""
      </section>
      <section class="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
        <h2 class="text-base font-bold text-slate-900 dark:text-white uppercase mb-3 flex items-center gap-2">
          🛡️ Certifications
        </h2>
    """

    for cert in certs:
        html += f"""
        <div class="text-sm">
          <div class="font-bold text-slate-900 dark:text-white">{cert.get("name")}</div>
          <div class="text-xs text-slate-500 dark:text-slate-400">{cert.get("issuer")} ({cert.get("date")})</div>
        </div>
        """

    html += """
      </section>
    </div>

    <!-- Footer -->
    <footer class="no-print text-center py-6 text-xs text-slate-400 dark:text-slate-500">
      Rendered via Multica Dynamic Artifact Framework &bull; Composable with <code class="px-1.5 py-0.5 rounded bg-slate-200 dark:bg-slate-800 font-mono">publish-to-trycloudflare</code>
    </footer>

  </div>

  <script>
    const toggle = document.getElementById('theme-toggle');
    toggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
    });
  </script>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="Multica Dynamic Artifact Generator")
    parser.add_argument("--data", required=True, help="Input JSON data file path")
    parser.add_argument("--preset", choices=["executive", "technical", "graphically_rich"], default="executive", help="Audience styling preset")
    parser.add_argument("--format", choices=["pdf", "svg", "html", "all"], default="all", help="Output format")
    parser.add_argument("--output-dir", default="./dist", help="Output directory path")
    args = parser.parse_args()

    script_dir = get_script_dir()
    templates_dir = os.path.abspath(os.path.join(script_dir, "../templates"))
    os.makedirs(args.output_dir, exist_ok=True)
    dist_abs = os.path.abspath(args.output_dir)
    data_abs = os.path.abspath(args.data)

    if not os.path.exists(data_abs):
        print(f"Error: Input data file '{data_abs}' does not exist.", file=sys.stderr)
        sys.exit(1)

    template_file = os.path.join(templates_dir, f"{args.preset}.typ")
    if not os.path.exists(template_file):
        print(f"Error: Template for preset '{args.preset}' not found at '{template_file}'.", file=sys.stderr)
        sys.exit(1)

    typst_bin = ensure_typst_binary()

    base_name = f"artifact_{args.preset}"
    print(f"=== Multica Dynamic Artifact Generator ===")
    print(f"Engine:    {typst_bin}")
    print(f"Input:     {data_abs}")
    print(f"Preset:    {args.preset}")
    print(f"Format:    {args.format}")
    print(f"Output:    {dist_abs}")
    print("-------------------------------------------")

    # PDF Output
    if args.format in ["pdf", "all"]:
        pdf_path = os.path.join(dist_abs, f"{base_name}.pdf")
        t0 = time.perf_counter()
        cmd = [typst_bin, "compile", "--root", "/", "--input", f"data_file={data_abs}", template_file, pdf_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Typst compilation failed:\n{res.stderr}", file=sys.stderr)
            sys.exit(res.returncode)
        duration = (time.perf_counter() - t0) * 1000
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"✓ PDF Document:  {pdf_path} ({size_kb:.1f} KB in {duration:.1f} ms)")

    # SVG Output
    if args.format in ["svg", "all"]:
        svg_pattern = os.path.join(dist_abs, f"{base_name}_page_{{p}}.svg")
        t0 = time.perf_counter()
        cmd = [typst_bin, "compile", "--root", "/", "--input", f"data_file={data_abs}", template_file, svg_pattern]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Typst SVG compilation failed:\n{res.stderr}", file=sys.stderr)
            sys.exit(res.returncode)
        duration = (time.perf_counter() - t0) * 1000
        print(f"✓ SVG Vector:    {svg_pattern} (rendered in {duration:.1f} ms)")

    # HTML Output
    if args.format in ["html", "all"]:
        html_path = os.path.join(dist_abs, f"{base_name}_web.html")
        t0 = time.perf_counter()
        generate_interactive_html(data_abs, html_path, preset=args.preset)
        duration = (time.perf_counter() - t0) * 1000
        size_kb = os.path.getsize(html_path) / 1024
        print(f"✓ Web HTML:      {html_path} ({size_kb:.1f} KB in {duration:.1f} ms)")

    print("-------------------------------------------")
    print("Generation completed successfully.")

if __name__ == "__main__":
    main()
