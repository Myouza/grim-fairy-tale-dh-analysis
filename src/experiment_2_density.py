"""
Experiment 2: Narrative Density Heatmap Analysis

Research Question:
How does RPG Maker's spatial architecture structure storytelling?

Theoretical Grounding:
- Platform studies (Montfort & Bogost)
- Spatial narratology (Jenkins, Tally)
- Game design analysis (Juul, Aarseth)

Method:
1. Parse EventTextDump.txt to count commands by type per map
2. Calculate narrative density = dialogue_count / total_commands
3. Classify maps by density (Story-Heavy, Mixed, Combat/Traversal)
4. Visualize spatial distribution of narrative content
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

from .visualization import (
    create_figure, save_figure, add_source_annotation,
    save_table_markdown, save_table_csv,
    COLORS, get_classification_color, setup_style
)
from .parsers import EventDumpParser, save_json_data


class NarrativeDensity:
    """
    Analyze narrative density across game maps.
    
    Calculates the ratio of dialogue commands to total commands for each map,
    revealing patterns of narrative concentration in spatial game design.
    
    Attributes:
        parser: EventDumpParser instance
        density_df: DataFrame with density calculations per map
        statistics: Summary statistics dictionary
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize density analyzer.
        
        Args:
            data_dir: Path to data directory
        """
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / 'data'
        self.output_dir = Path(__file__).parent.parent / 'outputs'
        
        self.parser = EventDumpParser()
        self.density_df: Optional[pd.DataFrame] = None
        self.statistics: Dict[str, Any] = {}
        
    def load_and_parse(self):
        """Load and parse EventTextDump.txt."""
        dump_path = self.data_dir / 'EventTextDump.txt'
        self.parser.parse_file(str(dump_path))
        
        # Calculate density for all maps
        self.density_df = self.parser.count_commands_by_map()
        
        # Filter to maps with content
        self.density_df = self.density_df[self.density_df['total_commands'] > 0]
        
        print(f"Parsed {len(self.parser.maps)} maps")
        print(f"Found {len(self.density_df)} maps with content")
        
    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Calculate summary statistics for narrative density.
        
        Returns:
            Dictionary of statistics
        """
        if self.density_df is None:
            self.load_and_parse()
        
        df = self.density_df
        
        self.statistics = {
            'total_maps': len(df),
            'mean_density': round(df['narrative_density'].mean(), 4),
            'median_density': round(df['narrative_density'].median(), 4),
            'std_density': round(df['narrative_density'].std(), 4),
            'min_density': round(df['narrative_density'].min(), 4),
            'max_density': round(df['narrative_density'].max(), 4),
            
            # Classification counts
            'story_heavy_count': int((df['classification'] == 'Story-Heavy').sum()),
            'mixed_count': int((df['classification'] == 'Mixed').sum()),
            'combat_traversal_count': int((df['classification'] == 'Combat/Traversal').sum()),
            
            # Percentages
            'story_heavy_pct': round((df['classification'] == 'Story-Heavy').mean() * 100, 2),
            'mixed_pct': round((df['classification'] == 'Mixed').mean() * 100, 2),
            'combat_traversal_pct': round((df['classification'] == 'Combat/Traversal').mean() * 100, 2),
            
            # Command totals
            'total_dialogue_commands': int(df['dialogue_count'].sum()),
            'total_battle_commands': int(df['battle_count'].sum()),
            'total_logic_commands': int(df['logic_count'].sum()),
            'total_all_commands': int(df['total_commands'].sum()),
        }
        
        # Top story-heavy maps
        top_story = df.nlargest(10, 'narrative_density')[['map_id', 'map_name', 'narrative_density']]
        self.statistics['top_story_maps'] = top_story.to_dict('records')
        
        # Top combat maps
        top_combat = df.nsmallest(10, 'narrative_density')[['map_id', 'map_name', 'narrative_density']]
        self.statistics['top_combat_maps'] = top_combat.to_dict('records')
        
        return self.statistics
    
    def plot_density_heatmap(self) -> plt.Figure:
        """
        Create horizontal bar chart of all maps by narrative density.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.density_df is None:
            self.load_and_parse()
        
        # Sort by density
        df = self.density_df.sort_values('narrative_density', ascending=True).copy()
        
        # Limit to maps with meaningful content (top 50 by total commands)
        df = df.nlargest(50, 'total_commands').sort_values('narrative_density', ascending=True)
        
        # Create tall figure
        fig_height = max(8, len(df) * 0.25)
        fig, ax = plt.subplots(figsize=(10, fig_height))
        
        # Color by classification
        colors = df['classification'].apply(get_classification_color)
        
        # Create bar chart
        y_pos = np.arange(len(df))
        bars = ax.barh(y_pos, df['narrative_density'], color=colors, edgecolor='white', linewidth=0.5)
        
        # Labels
        labels = [f"Map {row['map_id']:03d}: {row['map_name'][:15]}" for _, row in df.iterrows()]
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=8)
        
        ax.set_xlabel('Narrative Density (Dialogue / Total Commands)')
        ax.set_xlim(0, 1.0)
        ax.set_title('Narrative Density Across Game Maps\n(Top 50 Maps by Activity)', 
                     fontsize=14, fontweight='bold')
        
        # Add classification legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['story'], label=f'Story-Heavy (>{0.7:.0%})'),
            Patch(facecolor=COLORS['mixed'], label=f'Mixed ({0.3:.0%}-{0.7:.0%})'),
            Patch(facecolor=COLORS['combat'], label=f'Combat/Traversal (<{0.3:.0%})'),
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
        
        # Add vertical reference lines
        ax.axvline(x=0.3, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=0.7, color='gray', linestyle='--', alpha=0.5)
        
        add_source_annotation(ax, 'Source: EventTextDump.txt analysis')
        
        plt.tight_layout()
        
        return fig
    
    def plot_top_maps_comparison(self) -> plt.Figure:
        """
        Create two-panel comparison of story vs combat maps.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.density_df is None:
            self.load_and_parse()
        
        df = self.density_df
        
        # Get top 10 for each category
        top_story = df.nlargest(10, 'narrative_density')
        top_combat = df[df['narrative_density'] < 0.3].nsmallest(10, 'narrative_density')
        
        # If not enough combat maps, get lowest overall
        if len(top_combat) < 10:
            top_combat = df.nsmallest(10, 'narrative_density')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Story-heavy panel
        y_pos = np.arange(len(top_story))
        ax1.barh(y_pos, top_story['narrative_density'], color=COLORS['story'], 
                 edgecolor='white', linewidth=0.5)
        labels1 = [f"{row['map_name'][:20]}" for _, row in top_story.iterrows()]
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(labels1, fontsize=9)
        ax1.set_xlabel('Narrative Density')
        ax1.set_xlim(0, 1.0)
        ax1.set_title('Top 10 Story-Heavy Maps', fontsize=12, fontweight='bold')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(top_story['narrative_density']):
            ax1.text(v + 0.02, i, f'{v:.2f}', va='center', fontsize=9)
        
        # Combat/traversal panel
        y_pos = np.arange(len(top_combat))
        ax2.barh(y_pos, top_combat['narrative_density'], color=COLORS['combat'],
                 edgecolor='white', linewidth=0.5)
        labels2 = [f"{row['map_name'][:20]}" for _, row in top_combat.iterrows()]
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(labels2, fontsize=9)
        ax2.set_xlabel('Narrative Density')
        ax2.set_xlim(0, 0.5)  # Narrower range for combat
        ax2.set_title('Top 10 Combat/Traversal Maps', fontsize=12, fontweight='bold')
        ax2.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(top_combat['narrative_density']):
            ax2.text(v + 0.01, i, f'{v:.2f}', va='center', fontsize=9)
        
        fig.suptitle('Spatial Storytelling Patterns: Narrative Distribution', 
                     fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        return fig
    
    def plot_density_distribution(self) -> plt.Figure:
        """
        Create histogram and statistics visualization.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.density_df is None:
            self.load_and_parse()
        
        df = self.density_df
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Histogram
        ax1.hist(df['narrative_density'], bins=20, color=COLORS['mixed'], 
                 edgecolor='white', alpha=0.8)
        ax1.axvline(df['narrative_density'].mean(), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean: {df["narrative_density"].mean():.2f}')
        ax1.axvline(df['narrative_density'].median(), color='blue', linestyle='--', 
                    linewidth=2, label=f'Median: {df["narrative_density"].median():.2f}')
        ax1.set_xlabel('Narrative Density')
        ax1.set_ylabel('Number of Maps')
        ax1.set_title('Distribution of Narrative Density', fontsize=12, fontweight='bold')
        ax1.legend(loc='upper right')
        
        # Add threshold lines
        ax1.axvline(x=0.3, color='gray', linestyle=':', alpha=0.7)
        ax1.axvline(x=0.7, color='gray', linestyle=':', alpha=0.7)
        
        # Pie chart of classifications
        class_counts = df['classification'].value_counts()
        colors = [get_classification_color(c) for c in class_counts.index]
        
        wedges, texts, autotexts = ax2.pie(
            class_counts.values, 
            labels=class_counts.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05] * len(class_counts)
        )
        ax2.set_title('Map Classification Distribution', fontsize=12, fontweight='bold')
        
        # Make percentage text more visible
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.tight_layout()
        
        return fig
    
    def plot_command_breakdown(self) -> plt.Figure:
        """
        Create stacked bar chart showing command type breakdown by map category.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.density_df is None:
            self.load_and_parse()
        
        df = self.density_df
        
        # Aggregate by classification
        agg_data = df.groupby('classification').agg({
            'dialogue_count': 'sum',
            'battle_count': 'sum',
            'logic_count': 'sum',
            'navigation_count': 'sum',
            'visual_audio_count': 'sum',
            'other_count': 'sum'
        })
        
        # Calculate percentages
        totals = agg_data.sum(axis=1)
        agg_pct = agg_data.div(totals, axis=0) * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Story-Heavy', 'Mixed', 'Combat/Traversal']
        categories = [c for c in categories if c in agg_pct.index]
        
        x = np.arange(len(categories))
        width = 0.5
        
        # Create stacked bars
        command_types = ['dialogue_count', 'battle_count', 'logic_count', 
                        'navigation_count', 'visual_audio_count', 'other_count']
        labels = ['Dialogue', 'Battle', 'Logic', 'Navigation', 'Visual/Audio', 'Other']
        colors = ['#E74C3C', '#3498DB', '#9B59B6', '#2ECC71', '#F39C12', '#95A5A6']
        
        bottom = np.zeros(len(categories))
        
        for cmd_type, label, color in zip(command_types, labels, colors):
            values = [agg_pct.loc[cat, cmd_type] if cat in agg_pct.index else 0 
                     for cat in categories]
            ax.bar(x, values, width, bottom=bottom, label=label, color=color)
            bottom += values
        
        ax.set_ylabel('Percentage of Commands')
        ax.set_xlabel('Map Classification')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_title('Command Type Breakdown by Map Classification', 
                     fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    def run(self, maps=None) -> Dict[str, Any]:
        """
        Run complete narrative density analysis.
        
        Args:
            maps: Optional pre-parsed maps (unused, for interface compatibility)
            
        Returns:
            Dictionary with all results and file paths
        """
        print("="*60)
        print("EXPERIMENT 2: Narrative Density Heatmap Analysis")
        print("="*60)
        
        # Load and parse data
        print("\n[1/4] Loading and parsing EventTextDump.txt...")
        self.load_and_parse()
        
        # Calculate statistics
        print("[2/4] Calculating statistics...")
        stats = self.calculate_statistics()
        
        print(f"  - Total maps: {stats['total_maps']}")
        print(f"  - Mean density: {stats['mean_density']:.4f}")
        print(f"  - Story-heavy: {stats['story_heavy_count']} ({stats['story_heavy_pct']:.1f}%)")
        print(f"  - Mixed: {stats['mixed_count']} ({stats['mixed_pct']:.1f}%)")
        print(f"  - Combat/Traversal: {stats['combat_traversal_count']} ({stats['combat_traversal_pct']:.1f}%)")
        
        # Generate visualizations
        print("[3/4] Generating visualizations...")
        
        # Figure 1: Density heatmap
        fig1 = self.plot_density_heatmap()
        fig1_paths = save_figure(fig1, self.output_dir / 'figures' / 'exp2_density_heatmap')
        plt.close(fig1)
        print(f"  - Saved: {fig1_paths}")
        
        # Figure 2: Top maps comparison
        fig2 = self.plot_top_maps_comparison()
        fig2_paths = save_figure(fig2, self.output_dir / 'figures' / 'exp2_top_maps_comparison')
        plt.close(fig2)
        print(f"  - Saved: {fig2_paths}")
        
        # Figure 3: Distribution
        fig3 = self.plot_density_distribution()
        fig3_paths = save_figure(fig3, self.output_dir / 'figures' / 'exp2_density_distribution')
        plt.close(fig3)
        print(f"  - Saved: {fig3_paths}")
        
        # Figure 4: Command breakdown
        fig4 = self.plot_command_breakdown()
        fig4_paths = save_figure(fig4, self.output_dir / 'figures' / 'exp2_command_breakdown')
        plt.close(fig4)
        print(f"  - Saved: {fig4_paths}")
        
        # Save tables and metrics
        print("[4/4] Saving tables and metrics...")
        
        # Full density table
        table_df = self.density_df[['map_id', 'map_name', 'dialogue_count', 'total_commands',
                                     'narrative_density', 'classification']].sort_values(
            'narrative_density', ascending=False
        )
        md_path = save_table_markdown(table_df, 
                                       self.output_dir / 'tables' / 'exp2_density_table.md',
                                       'Narrative Density by Map')
        csv_path = save_table_csv(table_df, self.output_dir / 'tables' / 'exp2_density_table.csv')
        print(f"  - Saved: {md_path}")
        print(f"  - Saved: {csv_path}")
        
        # Metrics JSON
        metrics_path = self.output_dir / 'metrics' / 'exp2_density_metrics.json'
        save_json_data(stats, str(metrics_path))
        print(f"  - Saved: {metrics_path}")
        
        print("\n✓ Experiment 2 complete!")
        
        return {
            'metrics': stats,
            'figures': fig1_paths + fig2_paths + fig3_paths + fig4_paths,
            'tables': [md_path, csv_path],
            'metrics_file': str(metrics_path)
        }


if __name__ == '__main__':
    # Run experiment standalone
    exp = NarrativeDensity()
    results = exp.run()
    print("\nKey Statistics:")
    for key in ['mean_density', 'story_heavy_pct', 'mixed_pct', 'combat_traversal_pct']:
        print(f"  {key}: {results['metrics'][key]}")
