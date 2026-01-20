"""
Experiment 4: Motif Evolution Analysis

Research Question:
How does the "Red Hood" symbol's meaning shift across narrative arcs?

Theoretical Grounding:
- Catherine Orenstein's *Little Red Riding Hood Uncloaked*
- Vladimir Propp's morphological analysis
- Diachronic motif tracking in folklore studies

Method:
1. Extract all mentions of "小红帽" from narrative
2. Define context keyword sets (Innocence, Military, Posthuman)
3. Score each mention's context
4. Track dominant context across arcs
5. Visualize semantic drift
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from .visualization import (
    create_figure, save_figure, add_source_annotation,
    save_table_markdown, save_table_csv,
    COLORS, get_context_color, setup_style
)
from .parsers import EventDumpParser, load_json_data, save_json_data


class MotifEvolution:
    """
    Track semantic evolution of the "Red Hood" motif across narrative arcs.
    
    Analyzes how the symbol's meaning shifts between innocence, military,
    and posthuman contexts throughout the game narrative.
    
    Attributes:
        motif: Target motif to track (default: "小红帽")
        context_keywords: Dictionary of context categories and their keywords
        instances: List of motif instance dictionaries with context scores
        evolution_df: DataFrame showing context evolution across arcs
    """
    
    def __init__(self, motif: str = "小红帽", data_dir: Optional[str] = None):
        """
        Initialize motif tracker.
        
        Args:
            motif: Target motif string to track
            data_dir: Path to data directory
        """
        self.motif = motif
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / 'data'
        self.output_dir = Path(__file__).parent.parent / 'outputs'
        
        self.context_keywords: Dict[str, List[str]] = {}
        self.instances: List[Dict[str, Any]] = []
        self.evolution_df: Optional[pd.DataFrame] = None
        
    def load_context_keywords(self):
        """Load context keyword sets from context_keywords.json."""
        context_path = self.data_dir / 'context_keywords.json'
        context_data = load_json_data(str(context_path))
        
        self.context_keywords = context_data.get('motif_contexts', {
            'innocence': ['外婆', '罐头', '家', '想你', '梦见', '回来', '小时候'],
            'military': ['团长', '战斗', '狼人', '士兵', '命令', '战争', '敌人'],
            'posthuman': ['血', '病毒', '基因', '吸血鬼', '感染', '培育', '死']
        })
        
        print(f"Loaded context keywords:")
        for category, keywords in self.context_keywords.items():
            print(f"  - {category}: {len(keywords)} keywords")
    
    def extract_instances(self) -> List[Dict[str, Any]]:
        """
        Extract all instances of the motif from game dialogue.
        
        Returns:
            List of instance dictionaries with context scores
        """
        # Parse event dump
        parser = EventDumpParser()
        parser.parse_file(str(self.data_dir / 'EventTextDump.txt'))
        dialogues = parser.extract_all_dialogue()
        
        self.instances = []
        
        for dialogue in dialogues:
            text = dialogue.get('text', '') or ''
            
            # Check if motif is present
            if self.motif not in text:
                continue
            
            # Score contexts
            scores = {}
            for category, keywords in self.context_keywords.items():
                score = sum(1 for kw in keywords if kw in text)
                scores[category] = score
            
            # Determine dominant context
            total = sum(scores.values())
            if total > 0:
                dominant = max(scores, key=scores.get)
            else:
                dominant = 'neutral'
            
            # Determine arc from map_id
            arc = self._map_to_arc(dialogue['map_id'])
            
            self.instances.append({
                'map_id': dialogue['map_id'],
                'map_name': dialogue['map_name'],
                'event_id': dialogue['event_id'],
                'line': dialogue['line'],
                'text': text[:150],  # First 150 chars
                'arc': arc,
                'scores': scores,
                'dominant_context': dominant,
                'total_context_score': total
            })
        
        print(f"Found {len(self.instances)} motif instances")
        return self.instances
    
    def _map_to_arc(self, map_id: int) -> str:
        """
        Determine narrative arc from map ID.
        
        This is based on the game's structure where:
        - Maps 1-45: Chapter 1 (Little Red)
        - Maps 46-100: Chapter 2 (Cinderella)  
        - Maps 101+: Chapter 3 (Snow White)
        
        Within Chapter 1:
        - Maps 1-10: Arc 1.1 (Camp/Departure)
        - Maps 11-30: Arc 1.2 (Journey)
        - Maps 31-45: Arc 1.3 (Grandmother)
        
        Args:
            map_id: Map ID number
            
        Returns:
            Arc identifier string
        """
        if map_id <= 10:
            return '1.1 (Camp)'
        elif map_id <= 30:
            return '1.2 (Journey)'
        elif map_id <= 45:
            return '1.3 (Grandmother)'
        elif map_id <= 100:
            return '2.x (Cinderella)'
        else:
            return '3.x (Snow White)'
    
    def analyze_evolution(self) -> pd.DataFrame:
        """
        Calculate context distribution per arc.
        
        Returns:
            DataFrame with percentage breakdown by arc
        """
        arc_contexts = defaultdict(lambda: defaultdict(int))
        
        for instance in self.instances:
            arc = instance['arc']
            context = instance['dominant_context']
            arc_contexts[arc][context] += 1
        
        # Convert to percentages
        evolution_data = []
        
        for arc in sorted(arc_contexts.keys()):
            counts = arc_contexts[arc]
            total = sum(counts.values())
            
            row = {
                'Arc': arc,
                'Innocence %': round((counts.get('innocence', 0) / total * 100), 1) if total > 0 else 0,
                'Military %': round((counts.get('military', 0) / total * 100), 1) if total > 0 else 0,
                'Posthuman %': round((counts.get('posthuman', 0) / total * 100), 1) if total > 0 else 0,
                'Neutral %': round((counts.get('neutral', 0) / total * 100), 1) if total > 0 else 0,
                'Total Instances': total
            }
            
            # Determine dominant context for this arc
            contexts = ['innocence', 'military', 'posthuman', 'neutral']
            dominant = max(contexts, key=lambda c: counts.get(c, 0))
            row['Dominant Context'] = dominant.title()
            
            evolution_data.append(row)
        
        self.evolution_df = pd.DataFrame(evolution_data)
        return self.evolution_df
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive motif analysis metrics.
        
        Returns:
            Dictionary of metrics
        """
        if not self.instances:
            self.extract_instances()
        
        if self.evolution_df is None:
            self.analyze_evolution()
        
        # Overall statistics
        metrics = {
            'motif': self.motif,
            'total_instances': len(self.instances),
            'unique_arcs': len(self.evolution_df) if self.evolution_df is not None else 0
        }
        
        # Context distribution across all instances
        context_totals = defaultdict(int)
        for inst in self.instances:
            context_totals[inst['dominant_context']] += 1
        
        total = sum(context_totals.values())
        for context, count in context_totals.items():
            metrics[f'{context}_total_pct'] = round(count / total * 100, 2) if total > 0 else 0
        
        # Semantic shift analysis
        if self.evolution_df is not None and len(self.evolution_df) >= 2:
            first_arc = self.evolution_df.iloc[0]
            last_arc = self.evolution_df.iloc[-1]
            
            metrics['initial_dominant'] = first_arc['Dominant Context']
            metrics['final_dominant'] = last_arc['Dominant Context']
            
            # Calculate shift in each context
            for context in ['Innocence', 'Military', 'Posthuman']:
                col = f'{context} %'
                shift = last_arc[col] - first_arc[col]
                metrics[f'{context.lower()}_shift'] = round(shift, 2)
        
        # Add evolution table as records
        if self.evolution_df is not None:
            metrics['arc_evolution'] = self.evolution_df.to_dict('records')
        
        return metrics
    
    def plot_stacked_area(self) -> plt.Figure:
        """
        Create stacked area chart showing context evolution.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.evolution_df is None:
            self.analyze_evolution()
        
        if len(self.evolution_df) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No motif data available', ha='center', va='center')
            ax.axis('off')
            return fig
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        df = self.evolution_df
        
        x = range(len(df))
        
        # Stack the context percentages
        innocence = df['Innocence %'].values
        military = df['Military %'].values
        posthuman = df['Posthuman %'].values
        neutral = df['Neutral %'].values
        
        ax.stackplot(x, innocence, military, posthuman, neutral,
                    labels=['Innocence', 'Military', 'Posthuman', 'Neutral'],
                    colors=[COLORS['innocence'], COLORS['military'], 
                           COLORS['posthuman'], COLORS['neutral']],
                    alpha=0.8)
        
        ax.set_xticks(x)
        ax.set_xticklabels(df['Arc'], rotation=30, ha='right', fontsize=10)
        ax.set_xlabel('Narrative Arc')
        ax.set_ylabel('Context Distribution (%)')
        ax.set_ylim(0, 100)
        ax.set_title(f'Semantic Evolution of "{self.motif}" Across Narrative Arcs',
                     fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        
        # Add instance count annotations
        for i, row in df.iterrows():
            ax.annotate(f'n={row["Total Instances"]}', 
                       (i, 5), 
                       ha='center', 
                       fontsize=8,
                       color='white',
                       fontweight='bold')
        
        add_source_annotation(ax, 'Source: EventTextDump.txt analysis')
        
        plt.tight_layout()
        
        return fig
    
    def plot_context_bars(self) -> plt.Figure:
        """
        Create grouped bar chart for context distribution by arc.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.evolution_df is None:
            self.analyze_evolution()
        
        if len(self.evolution_df) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No motif data available', ha='center', va='center')
            ax.axis('off')
            return fig
        
        df = self.evolution_df
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(df))
        width = 0.2
        
        # Create bars for each context
        ax.bar(x - 1.5*width, df['Innocence %'], width, 
               label='Innocence', color=COLORS['innocence'])
        ax.bar(x - 0.5*width, df['Military %'], width,
               label='Military', color=COLORS['military'])
        ax.bar(x + 0.5*width, df['Posthuman %'], width,
               label='Posthuman', color=COLORS['posthuman'])
        ax.bar(x + 1.5*width, df['Neutral %'], width,
               label='Neutral', color=COLORS['neutral'])
        
        ax.set_xlabel('Narrative Arc')
        ax.set_ylabel('Percentage (%)')
        ax.set_title(f'Context Distribution for "{self.motif}" by Arc',
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Arc'], rotation=30, ha='right', fontsize=10)
        ax.legend(loc='upper right', fontsize=10)
        ax.set_ylim(0, 100)
        
        plt.tight_layout()
        
        return fig
    
    def plot_transition_flow(self) -> plt.Figure:
        """
        Create a simplified Sankey-like flow diagram showing context transitions.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.evolution_df is None or len(self.evolution_df) < 2:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.text(0.5, 0.5, 'Insufficient data for transition flow', ha='center', va='center')
            ax.axis('off')
            return fig
        
        df = self.evolution_df
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Position arcs horizontally
        n_arcs = len(df)
        arc_x = np.linspace(0.1, 0.9, n_arcs)
        
        # Context colors
        context_colors = {
            'Innocence': COLORS['innocence'],
            'Military': COLORS['military'],
            'Posthuman': COLORS['posthuman'],
            'Neutral': COLORS['neutral']
        }
        
        contexts = ['Innocence', 'Military', 'Posthuman', 'Neutral']
        
        # Draw boxes for each arc showing context distribution
        box_height = 0.7
        box_width = 0.08
        
        for i, (idx, row) in enumerate(df.iterrows()):
            x = arc_x[i]
            
            # Draw stacked bars within arc
            y_start = 0.15
            for context in contexts:
                pct = row[f'{context} %'] / 100 * box_height
                if pct > 0:
                    rect = plt.Rectangle((x - box_width/2, y_start), box_width, pct,
                                         facecolor=context_colors[context], 
                                         edgecolor='white',
                                         linewidth=1)
                    ax.add_patch(rect)
                    
                    # Add percentage label if significant
                    if row[f'{context} %'] >= 15:
                        ax.text(x, y_start + pct/2, 
                               f'{row[f"{context} %"]:.0f}%',
                               ha='center', va='center', fontsize=8,
                               fontweight='bold', color='white')
                    
                    y_start += pct
            
            # Arc label
            ax.text(x, 0.05, row['Arc'], ha='center', va='top', fontsize=9, rotation=30)
            ax.text(x, 0.9, f'n={row["Total Instances"]}', ha='center', va='bottom', fontsize=8)
        
        # Draw transition lines between arcs
        for i in range(n_arcs - 1):
            x1, x2 = arc_x[i] + box_width/2, arc_x[i+1] - box_width/2
            
            # Draw lines for each context weighted by percentage
            for context in contexts:
                pct1 = df.iloc[i][f'{context} %']
                pct2 = df.iloc[i+1][f'{context} %']
                
                if pct1 > 10 and pct2 > 10:  # Only show significant flows
                    y1 = 0.15 + (pct1 / 200) * box_height  # Midpoint
                    y2 = 0.15 + (pct2 / 200) * box_height
                    
                    # Line thickness based on average percentage
                    linewidth = (pct1 + pct2) / 20
                    
                    ax.plot([x1, x2], [y1, y2], 
                           color=context_colors[context],
                           linewidth=linewidth,
                           alpha=0.5)
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=context) 
                          for context, color in context_colors.items()]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title(f'Semantic Drift: "{self.motif}" Context Transitions',
                     fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    def plot_instance_timeline(self) -> plt.Figure:
        """
        Create timeline showing individual instances colored by context.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if not self.instances:
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.text(0.5, 0.5, 'No instances found', ha='center', va='center')
            ax.axis('off')
            return fig
        
        fig, ax = plt.subplots(figsize=(14, 4))
        
        # Sort instances by line number (proxy for narrative order)
        sorted_instances = sorted(self.instances, key=lambda x: x['line'])
        
        x = range(len(sorted_instances))
        colors = [get_context_color(inst['dominant_context']) for inst in sorted_instances]
        
        # Scatter plot of instances
        ax.scatter(x, [1]*len(x), c=colors, s=50, alpha=0.7, edgecolor='white')
        
        # Add arc boundaries
        prev_arc = None
        arc_boundaries = []
        for i, inst in enumerate(sorted_instances):
            if inst['arc'] != prev_arc:
                arc_boundaries.append((i, inst['arc']))
                prev_arc = inst['arc']
        
        for i, (boundary, arc) in enumerate(arc_boundaries):
            ax.axvline(x=boundary, color='gray', linestyle='--', alpha=0.5)
            if i < len(arc_boundaries) - 1:
                mid = (boundary + arc_boundaries[i+1][0]) / 2
            else:
                mid = (boundary + len(sorted_instances)) / 2
            ax.text(mid, 1.3, arc, ha='center', va='bottom', fontsize=9, rotation=30)
        
        ax.set_xlim(-1, len(sorted_instances))
        ax.set_ylim(0.5, 1.6)
        ax.set_xlabel('Instance (Chronological Order)')
        ax.set_yticks([])
        ax.set_title(f'Timeline of "{self.motif}" Mentions (Colored by Context)',
                     fontsize=14, fontweight='bold')
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['innocence'], label='Innocence'),
            Patch(facecolor=COLORS['military'], label='Military'),
            Patch(facecolor=COLORS['posthuman'], label='Posthuman'),
            Patch(facecolor=COLORS['neutral'], label='Neutral'),
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9, ncol=4)
        
        plt.tight_layout()
        
        return fig
    
    def run(self, beats=None) -> Dict[str, Any]:
        """
        Run complete motif evolution analysis.
        
        Args:
            beats: Optional pre-parsed beats (unused, for interface compatibility)
            
        Returns:
            Dictionary with all results and file paths
        """
        print("="*60)
        print("EXPERIMENT 4: Motif Evolution Analysis")
        print("="*60)
        
        # Load context keywords
        print(f"\n[1/4] Loading context keywords...")
        self.load_context_keywords()
        
        # Extract motif instances
        print(f"[2/4] Extracting instances of '{self.motif}'...")
        self.extract_instances()
        
        # Analyze evolution
        print("[3/4] Analyzing semantic evolution...")
        self.analyze_evolution()
        metrics = self.get_metrics()
        
        if 'initial_dominant' in metrics:
            print(f"  - Initial dominant context: {metrics['initial_dominant']}")
            print(f"  - Final dominant context: {metrics['final_dominant']}")
            print(f"  - Innocence shift: {metrics.get('innocence_shift', 0):+.1f}%")
            print(f"  - Military shift: {metrics.get('military_shift', 0):+.1f}%")
            print(f"  - Posthuman shift: {metrics.get('posthuman_shift', 0):+.1f}%")
        
        # Generate visualizations
        print("[4/4] Generating visualizations...")
        
        # Figure 1: Stacked area chart
        fig1 = self.plot_stacked_area()
        fig1_paths = save_figure(fig1, self.output_dir / 'figures' / 'exp4_context_evolution')
        plt.close(fig1)
        print(f"  - Saved: {fig1_paths}")
        
        # Figure 2: Context bars
        fig2 = self.plot_context_bars()
        fig2_paths = save_figure(fig2, self.output_dir / 'figures' / 'exp4_context_bars')
        plt.close(fig2)
        print(f"  - Saved: {fig2_paths}")
        
        # Figure 3: Transition flow
        fig3 = self.plot_transition_flow()
        fig3_paths = save_figure(fig3, self.output_dir / 'figures' / 'exp4_transition_flow')
        plt.close(fig3)
        print(f"  - Saved: {fig3_paths}")
        
        # Figure 4: Instance timeline
        fig4 = self.plot_instance_timeline()
        fig4_paths = save_figure(fig4, self.output_dir / 'figures' / 'exp4_instance_timeline')
        plt.close(fig4)
        print(f"  - Saved: {fig4_paths}")
        
        # Save tables and metrics
        print("  Saving tables and metrics...")
        
        # Evolution table
        if self.evolution_df is not None and len(self.evolution_df) > 0:
            md_path = save_table_markdown(self.evolution_df, 
                                           self.output_dir / 'tables' / 'exp4_evolution_table.md',
                                           f'Motif Context Distribution: {self.motif}')
            csv_path = save_table_csv(self.evolution_df, 
                                       self.output_dir / 'tables' / 'exp4_evolution_table.csv')
            print(f"  - Saved: {md_path}")
            print(f"  - Saved: {csv_path}")
        else:
            md_path = csv_path = None
        
        # Metrics JSON
        metrics_path = self.output_dir / 'metrics' / 'exp4_motif_metrics.json'
        save_json_data(metrics, str(metrics_path))
        print(f"  - Saved: {metrics_path}")
        
        print("\n✓ Experiment 4 complete!")
        
        return {
            'metrics': metrics,
            'figures': fig1_paths + fig2_paths + fig3_paths + fig4_paths,
            'tables': [md_path, csv_path] if md_path else [],
            'metrics_file': str(metrics_path)
        }


if __name__ == '__main__':
    # Run experiment standalone
    exp = MotifEvolution()
    results = exp.run()
    print("\nKey Findings:")
    print(f"  Total instances: {results['metrics']['total_instances']}")
    if 'initial_dominant' in results['metrics']:
        print(f"  Initial context: {results['metrics']['initial_dominant']}")
        print(f"  Final context: {results['metrics']['final_dominant']}")
