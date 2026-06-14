#!/usr/bin/env python3
"""
run.py - headless runner for the Link Intel Suite (also the grader's entry point).

Runs the full internal-linking analysis on a Screaming Frog export with no Claude Code:
  load -> graph -> anchors -> topics -> entities (TF proxy) -> recommend (candidates)
       -> write report.json + report.html
"""
from __future__ import annotations
import argparse, os, sys, time, json, urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mcp"))
sys.path.insert(0, HERE)
import server  # the MCP server module exposes every tool as a function


def _call_model(prompt: str) -> str:
    """Call Ollama's Gemma model to generate a concise cluster name."""
    url = "http://localhost:11434/api/generate"
    payload = json.dumps({
        "model": "qwen3:4b",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 20, "temperature": 0.1}
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data.get("response", "").strip().replace('"', '').replace("'", "")
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export_dir")
    ap.add_argument("--no-dashboard", action="store_true")
    args = ap.parse_args()

    if not args.no_dashboard:
        server.start_dashboard()
        print(f"[li] dashboard: http://localhost:{server.PORT}", flush=True)
        time.sleep(1)

    t0 = time.time()
    server.li_load(args.export_dir)
    server.li_graph()
    server.li_anchors()

    # 1. Compute deterministic clusters
    server.li_topics()

    # 2. Orchestrate cluster naming (Topic Agent)
    clusters = server._A["clusters"]["clusters"]
    names_map = {}
    model_calls = 0

    for c in clusters:
        hub = c.get("hub_page") or "root"
        kws = ", ".join(c.get("keywords", []))
        size = c.get("size", 0)

        prompt = (f"Assign a professional, concise name (2-5 words) to an SEO topical cluster.\n"
                  f"Hub Page: {hub}\n"
                  f"Key Terms: {kws}\n"
                  f"Member Count: {size}\n"
                  f"Return ONLY the name. No quotes or explanations.")

        name = _call_model(prompt)
        if name:
            names_map[c["key"]] = name
            model_calls += 1
        else:
            names_map[c["key"]] = c["key"]

    # Commit names back to the server
    server.li_topics(names=names_map)

    server.li_entities()      # uses TF-keyword relatedness proxy
    # Starter does NOT attach model-written recs; _report_obj() then falls back to the
    # deterministic candidates (no anchors) so the contract always has data to grade.
    server.RUN["model_calls"] = model_calls
    server.RUN["duration_sec"] = round(time.time() - t0, 1)
    server.li_report()
    server.li_export()

    s = server.RUN["summary"]
    print("\n=== INTERNAL LINKING INTELLIGENCE ===")
    print(f"Site            : {server.RUN['site']}  ({s['pages_crawled']} pages)")
    print(f"Internal links  : {s['internal_links']}")
    print(f"Orphan pages    : {s['orphan_pages']}")
    print(f"Broken internal : {s['broken_internal_links']}")
    print(f"Generic anchors : {s['generic_anchors']}")
    print(f"Topical clusters: {s['topical_clusters']}")
    print(f"Link suggestions: {s['link_recommendations']}")
    print("Wrote outputs/report.json and outputs/report.html")


if __name__ == "__main__":
    main()
