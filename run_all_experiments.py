#!/usr/bin/env python3
"""
Run all DH experiments for Grim Fairy Tale analysis.

This script executes all four experiments in sequence:
1. Structural Alignment (film vs game comparison)
2. Narrative Density Heatmap (spatial storytelling)
3. Semantic Network Analysis (entity-theme co-occurrence)
4. Motif Evolution (Red Hood symbol tracking)

Usage:
    python run_all_experiments.py

All outputs are saved to:
    outputs/figures/  - PNG (300 DPI) and PDF figures
    outputs/tables/   - Markdown and CSV tables
    outputs/metrics/  - JSON metrics files
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.experiment_1_alignment import StructuralAlignment
from src.experiment_2_density import NarrativeDensity
from src.experiment_3_network import SemanticNetwork
from src.experiment_4_motif import MotifEvolution
from src.parsers import EventDumpParser, NarrativeExtractionParser


def print_header():
    """Print analysis header."""
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " GRIM FAIRY TALE: DIGITAL HUMANITIES ANALYSIS PIPELINE ".center(78) + "║")
    print("║" + " 小红帽 (Little Red Riding Hood) — Computational Analysis ".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()
    print(f"  Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_footer(results: dict, duration: float):
    """Print analysis footer with summary."""
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " ANALYSIS COMPLETE ".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()
    
    # Count outputs
    figure_count = sum(len(r.get('figures', [])) for r in results.values())
    table_count = sum(len(r.get('tables', [])) for r in results.values())
    metrics_count = len(results)
    
    print(f"  Duration: {duration:.1f} seconds")
    print()
    print("  Outputs Generated:")
    print(f"    • Figures: {figure_count} files (outputs/figures/)")
    print(f"    • Tables:  {table_count} files (outputs/tables/)")
    print(f"    • Metrics: {metrics_count} files (outputs/metrics/)")
    print()
    print("  Validation Metrics (Demonstration Values):")
    
    # Experiment 1 findings
    if 'exp1' in results and 'metrics' in results['exp1']:
        m = results['exp1']['metrics']
        print(f"    [Exp 1] Alignment testable: {m.get('alignment_score_percent', 'N/A')}% (for Ballad hypothesis)")
    
    # Experiment 2 findings
    if 'exp2' in results and 'metrics' in results['exp2']:
        m = results['exp2']['metrics']
        print(f"    [Exp 2] Spatial metrics calculable: {m.get('total_maps', 'N/A')} maps analyzed")
    
    # Experiment 3 findings
    if 'exp3' in results and 'metrics' in results['exp3']:
        m = results['exp3']['metrics']
        print(f"    [Exp 3] Network analysis operational: {m.get('num_nodes', 'N/A')} nodes, {m.get('num_communities', 'N/A')} communities")
    
    # Experiment 4 findings
    if 'exp4' in results and 'metrics' in results['exp4']:
        m = results['exp4']['metrics']
        print(f"    [Exp 4] Longitudinal tracking feasible: {m.get('total_instances', 'N/A')} motif instances tracked")
    
    print()
    print("  ┌─────────────────────────────────────────────────────────────────────┐")
    print("  │  NOTE: This is a PILOT STUDY demonstrating pipeline feasibility.   │")
    print("  │  See CAVEATS.md for interpretation guidelines.                      │")
    print("  │  Full research context: docs/research_context.md                    │")
    print("  └─────────────────────────────────────────────────────────────────────┘")
    print()
    print("  Documentation:")
    print("    • docs/methodology.md        — Two-stage validation design")
    print("    • docs/validation_results.md — What tests demonstrate")
    print("    • docs/research_context.md   — PhD research program context")
    print("    • CAVEATS.md                 — Interpretation guidelines")
    print()
    print("  Portfolio: https://myouza.github.io/phd-portfolio/")
    print()


def ensure_directories():
    """Create output directories if they don't exist."""
    dirs = [
        'outputs/figures',
        'outputs/tables', 
        'outputs/metrics'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def verify_data_files():
    """Verify that required data files exist."""
    required_files = [
        'data/EventTextDump.txt',
        'data/narrative_extraction.md',
        'data/ballad_of_soldier_beats.json',
        'data/context_keywords.json'
    ]
    
    missing = []
    for f in required_files:
        if not Path(f).exists():
            missing.append(f)
    
    if missing:
        print("ERROR: Missing required data files:")
        for f in missing:
            print(f"  - {f}")
        print()
        print("Please ensure all data files are in the data/ directory.")
        sys.exit(1)


def main():
    """Run all experiments."""
    start_time = time.time()
    
    print_header()
    
    # Setup
    ensure_directories()
    verify_data_files()
    
    results = {}
    
    # =========================================================================
    # Experiment 1: Structural Alignment
    # =========================================================================
    print("\n" + "─"*80)
    try:
        exp1 = StructuralAlignment()
        results['exp1'] = exp1.run()
    except Exception as e:
        print(f"ERROR in Experiment 1: {e}")
        results['exp1'] = {'error': str(e)}
    
    # =========================================================================
    # Experiment 2: Narrative Density
    # =========================================================================
    print("\n" + "─"*80)
    try:
        exp2 = NarrativeDensity()
        results['exp2'] = exp2.run()
    except Exception as e:
        print(f"ERROR in Experiment 2: {e}")
        results['exp2'] = {'error': str(e)}
    
    # =========================================================================
    # Experiment 3: Semantic Network
    # =========================================================================
    print("\n" + "─"*80)
    try:
        exp3 = SemanticNetwork()
        results['exp3'] = exp3.run()
    except Exception as e:
        print(f"ERROR in Experiment 3: {e}")
        results['exp3'] = {'error': str(e)}
    
    # =========================================================================
    # Experiment 4: Motif Evolution
    # =========================================================================
    print("\n" + "─"*80)
    try:
        exp4 = MotifEvolution()
        results['exp4'] = exp4.run()
    except Exception as e:
        print(f"ERROR in Experiment 4: {e}")
        results['exp4'] = {'error': str(e)}
    
    # =========================================================================
    # Summary
    # =========================================================================
    duration = time.time() - start_time
    print_footer(results, duration)
    
    return results


if __name__ == '__main__':
    main()
