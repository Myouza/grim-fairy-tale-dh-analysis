"""
Experiment 1: Structural Alignment Analysis

Research Question:
Is this game a systematic remediation of Grigori Chukhray's *Ballad of a Soldier* (1959)?

Theoretical Grounding:
- Marie-Laure Ryan's transmedial narratology
- Genette's theory of palimpsests  
- Structural formalism in adaptation studies

Method:
1. Encode key narrative beats from *Ballad of a Soldier*
2. Extract beats from game narrative
3. Match by structural type (heroic_act, reward, obligation, journey_delay, etc.)
4. Calculate alignment score and visualize correspondences
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

from .visualization import (
    create_figure, save_figure, add_source_annotation,
    save_table_markdown, save_table_csv,
    COLORS, setup_style
)
from .parsers import load_json_data, save_json_data


class StructuralAlignment:
    """
    Analyze structural alignment between game narrative and film source.
    
    Compares narrative beats from the game against the structure of
    *Ballad of a Soldier* (1959) to prove systematic remediation.
    
    Attributes:
        film_beats: List of film beat dictionaries
        game_beats: List of game beat dictionaries  
        alignment_table: DataFrame of matched beats
        alignment_score: Percentage of structural alignment
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize alignment analyzer.
        
        Args:
            data_dir: Path to data directory containing beat files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / 'data'
        self.output_dir = Path(__file__).parent.parent / 'outputs'
        
        self.film_beats: List[Dict[str, Any]] = []
        self.game_beats: List[Dict[str, Any]] = []
        self.alignment_table: Optional[pd.DataFrame] = None
        self.alignment_score: float = 0.0
        
    def load_data(self):
        """Load film and game beat data from JSON files."""
        # Load film beats
        film_path = self.data_dir / 'ballad_of_soldier_beats.json'
        self.film_beats = load_json_data(str(film_path))
        
        # Load game beats from context_keywords.json
        context_path = self.data_dir / 'context_keywords.json'
        context_data = load_json_data(str(context_path))
        self.game_beats = context_data.get('game_beats', [])
        
        print(f"Loaded {len(self.film_beats)} film beats")
        print(f"Loaded {len(self.game_beats)} game beats")
        
    def compute_alignment(self) -> pd.DataFrame:
        """
        Match narrative beats between film and game by structural type.
        
        Returns:
            DataFrame with alignment mappings
        """
        alignment_data = []
        
        # Group beats by type
        film_by_type = defaultdict(list)
        for fb in self.film_beats:
            film_by_type[fb['type']].append(fb)
        
        game_by_type = defaultdict(list)
        for gb in self.game_beats:
            game_by_type[gb['type']].append(gb)
        
        # Find matches
        for beat_type in film_by_type.keys():
            film_instances = film_by_type[beat_type]
            game_instances = game_by_type.get(beat_type, [])
            
            for fb in film_instances:
                if game_instances:
                    # Match to first available game instance
                    gb = game_instances[0]
                    match_type = self._classify_match(fb, gb)
                    
                    alignment_data.append({
                        'Beat Type': beat_type.replace('_', ' ').title(),
                        'Film Timestamp': fb['timestamp'],
                        'Film Beat': fb['description'],
                        'Game Location': f"Map {gb['map_id']:03d}, Event {gb['event_id']:03d}, Line {gb['line']}",
                        'Game Beat': gb['description'],
                        'Match Type': match_type,
                        'Matched': True
                    })
                    
                    # Remove used game instance
                    game_instances = game_instances[1:]
                else:
                    # No matching game beat
                    alignment_data.append({
                        'Beat Type': beat_type.replace('_', ' ').title(),
                        'Film Timestamp': fb['timestamp'],
                        'Film Beat': fb['description'],
                        'Game Location': '—',
                        'Game Beat': '(No match)',
                        'Match Type': 'Unmatched',
                        'Matched': False
                    })
        
        self.alignment_table = pd.DataFrame(alignment_data)
        
        # Sort by film timestamp
        self.alignment_table['_sort_key'] = self.alignment_table['Film Timestamp'].apply(
            lambda x: self._timestamp_to_minutes(x)
        )
        self.alignment_table = self.alignment_table.sort_values('_sort_key').drop('_sort_key', axis=1)
        
        return self.alignment_table
    
    def _classify_match(self, film_beat: Dict, game_beat: Dict) -> str:
        """
        Classify match type based on similarity.
        
        Args:
            film_beat: Film beat dictionary
            game_beat: Game beat dictionary
            
        Returns:
            'Direct Transposition' or 'Structural Homology'
        """
        film_desc = film_beat['description'].lower()
        game_desc = game_beat['description'].lower()
        
        # Check for key shared terms
        film_words = set(film_desc.split())
        game_words = set(game_desc.split())
        
        # Look for strong semantic overlap
        overlap_words = {'kill', 'tank', 'wolf', 'werewolf', 'visit', 'mother',
                        'grandmother', 'leave', 'return', 'soap', 'letter',
                        'deliver', 'promise', 'train', 'journey', 'delay'}
        
        film_key = film_words & overlap_words
        game_key = game_words & overlap_words
        
        if film_key & game_key:
            return 'Direct Transposition'
        else:
            return 'Structural Homology'
    
    def _timestamp_to_minutes(self, timestamp: str) -> float:
        """Convert HH:MM:SS to minutes."""
        parts = timestamp.split(':')
        if len(parts) == 3:
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            return h * 60 + m + s / 60
        elif len(parts) == 2:
            m, s = int(parts[0]), int(parts[1])
            return m + s / 60
        return 0.0
    
    def calculate_alignment_score(self) -> float:
        """
        Calculate percentage of film beats that are matched in the game.
        
        Returns:
            Alignment score (0-100)
        """
        if self.alignment_table is None:
            self.compute_alignment()
        
        matched = self.alignment_table['Matched'].sum()
        total = len(self.alignment_table)
        
        self.alignment_score = (matched / total * 100) if total > 0 else 0.0
        
        return self.alignment_score
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive alignment metrics.
        
        Returns:
            Dictionary of alignment metrics
        """
        if self.alignment_table is None:
            self.compute_alignment()
        
        df = self.alignment_table
        
        metrics = {
            'total_film_beats': len(self.film_beats),
            'total_game_beats': len(self.game_beats),
            'matched_beats': int(df['Matched'].sum()),
            'unmatched_beats': int((~df['Matched']).sum()),
            'alignment_score_percent': round(self.calculate_alignment_score(), 2),
            'direct_transpositions': int((df['Match Type'] == 'Direct Transposition').sum()),
            'structural_homologies': int((df['Match Type'] == 'Structural Homology').sum()),
            'beat_types_present': df[df['Matched']]['Beat Type'].nunique(),
            'total_beat_types': df['Beat Type'].nunique()
        }
        
        # Beat type breakdown
        type_counts = df.groupby('Beat Type')['Matched'].sum().to_dict()
        metrics['beat_type_matches'] = {k: int(v) for k, v in type_counts.items()}
        
        return metrics
    
    def plot_timeline_alignment(self) -> plt.Figure:
        """
        Create timeline alignment visualization.
        
        Shows film beats on top row, game beats on bottom row,
        with connecting lines for matches.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.alignment_table is None:
            self.compute_alignment()
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Convert timestamps to positions
        df = self.alignment_table.copy()
        df['Film Minutes'] = df['Film Timestamp'].apply(self._timestamp_to_minutes)
        
        # Normalize to 0-1 scale
        max_time = df['Film Minutes'].max()
        df['X Position'] = df['Film Minutes'] / max_time
        
        # Plot film beats (top row, y=1)
        film_x = df['X Position'].values
        film_y = np.ones(len(film_x))
        
        ax.scatter(film_x, film_y, s=150, c=COLORS['direct'], 
                   marker='s', label='Film Beats', zorder=3, edgecolor='white', linewidth=2)
        
        # Plot game beats (bottom row, y=0), only matched ones
        matched = df[df['Matched']]
        game_x = matched['X Position'].values
        game_y = np.zeros(len(game_x))
        
        ax.scatter(game_x, game_y, s=150, c=COLORS['structural'], 
                   marker='o', label='Game Beats', zorder=3, edgecolor='white', linewidth=2)
        
        # Draw connecting lines for matches
        for idx, row in matched.iterrows():
            x = row['X Position']
            color = COLORS['direct'] if row['Match Type'] == 'Direct Transposition' else COLORS['structural']
            linestyle = '-' if row['Match Type'] == 'Direct Transposition' else '--'
            
            ax.plot([x, x], [0, 1], color=color, linestyle=linestyle, 
                    alpha=0.6, linewidth=2, zorder=1)
        
        # Add beat type labels
        for idx, row in df.iterrows():
            beat_type_short = row['Beat Type'][:12] + '...' if len(row['Beat Type']) > 12 else row['Beat Type']
            ax.annotate(beat_type_short, 
                       (row['X Position'], 1.1), 
                       rotation=45, ha='left', va='bottom', fontsize=8)
        
        # Formatting
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.3, 1.5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Game Narrative', 'Film: Ballad of a Soldier'])
        ax.set_xlabel('Narrative Progression')
        ax.set_title('Structural Alignment: Game vs. Ballad of a Soldier (1959)', 
                     fontsize=14, fontweight='bold')
        
        # Legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='s', color='w', markerfacecolor=COLORS['direct'], 
                   markersize=12, label='Film Beat'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['structural'], 
                   markersize=12, label='Game Beat'),
            Line2D([0], [0], color=COLORS['direct'], linestyle='-', 
                   linewidth=2, label='Direct Transposition'),
            Line2D([0], [0], color=COLORS['structural'], linestyle='--', 
                   linewidth=2, label='Structural Homology'),
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
        
        # Add score annotation
        score = self.calculate_alignment_score()
        ax.text(0.02, -0.2, f'Alignment Score: {score:.1f}%', 
                transform=ax.transAxes, fontsize=11, fontweight='bold')
        
        add_source_annotation(ax, 'Source: narrative_extraction.md analysis')
        
        plt.tight_layout()
        
        return fig
    
    def plot_beat_type_comparison(self) -> plt.Figure:
        """
        Create bar chart comparing beat types between film and game.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.alignment_table is None:
            self.compute_alignment()
        
        # Count beat types
        film_types = defaultdict(int)
        for fb in self.film_beats:
            film_types[fb['type'].replace('_', ' ').title()] += 1
        
        game_types = defaultdict(int)
        for gb in self.game_beats:
            game_types[gb['type'].replace('_', ' ').title()] += 1
        
        # Combine all types
        all_types = sorted(set(film_types.keys()) | set(game_types.keys()))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(all_types))
        width = 0.35
        
        film_counts = [film_types.get(t, 0) for t in all_types]
        game_counts = [game_types.get(t, 0) for t in all_types]
        
        bars1 = ax.bar(x - width/2, film_counts, width, label='Film', color=COLORS['direct'])
        bars2 = ax.bar(x + width/2, game_counts, width, label='Game', color=COLORS['structural'])
        
        ax.set_xlabel('Beat Type')
        ax.set_ylabel('Count')
        ax.set_title('Narrative Beat Type Comparison: Film vs. Game', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(all_types, rotation=45, ha='right')
        ax.legend()
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9)
        
        plt.tight_layout()
        
        return fig
    
    def run(self) -> Dict[str, Any]:
        """
        Run complete structural alignment analysis.
        
        Returns:
            Dictionary with all results and file paths
        """
        print("="*60)
        print("EXPERIMENT 1: Structural Alignment Analysis")
        print("="*60)
        
        # Load data
        print("\n[1/4] Loading data...")
        self.load_data()
        
        # Compute alignment
        print("[2/4] Computing alignment...")
        self.compute_alignment()
        metrics = self.get_metrics()
        
        print(f"  - Matched {metrics['matched_beats']}/{metrics['total_film_beats']} film beats")
        print(f"  - Alignment score: {metrics['alignment_score_percent']:.1f}%")
        print(f"  - Direct transpositions: {metrics['direct_transpositions']}")
        print(f"  - Structural homologies: {metrics['structural_homologies']}")
        
        # Generate visualizations
        print("[3/4] Generating visualizations...")
        
        # Figure 1: Timeline alignment
        fig1 = self.plot_timeline_alignment()
        fig1_paths = save_figure(fig1, self.output_dir / 'figures' / 'exp1_timeline_alignment')
        plt.close(fig1)
        print(f"  - Saved: {fig1_paths}")
        
        # Figure 2: Beat type comparison
        fig2 = self.plot_beat_type_comparison()
        fig2_paths = save_figure(fig2, self.output_dir / 'figures' / 'exp1_beat_type_comparison')
        plt.close(fig2)
        print(f"  - Saved: {fig2_paths}")
        
        # Save tables and metrics
        print("[4/4] Saving tables and metrics...")
        
        # Alignment table
        table_df = self.alignment_table[['Beat Type', 'Film Timestamp', 'Film Beat', 
                                          'Game Location', 'Game Beat', 'Match Type']]
        md_path = save_table_markdown(table_df, 
                                       self.output_dir / 'tables' / 'exp1_alignment_table.md',
                                       'Structural Alignment: Film vs. Game Beats')
        csv_path = save_table_csv(table_df, self.output_dir / 'tables' / 'exp1_alignment_table.csv')
        print(f"  - Saved: {md_path}")
        print(f"  - Saved: {csv_path}")
        
        # Metrics JSON
        metrics_path = self.output_dir / 'metrics' / 'exp1_alignment_metrics.json'
        save_json_data(metrics, str(metrics_path))
        print(f"  - Saved: {metrics_path}")
        
        print("\n✓ Experiment 1 complete!")
        
        return {
            'metrics': metrics,
            'figures': fig1_paths + fig2_paths,
            'tables': [md_path, csv_path],
            'metrics_file': str(metrics_path)
        }


if __name__ == '__main__':
    # Run experiment standalone
    exp = StructuralAlignment()
    results = exp.run()
    print("\nResults:", json.dumps(results['metrics'], indent=2))
