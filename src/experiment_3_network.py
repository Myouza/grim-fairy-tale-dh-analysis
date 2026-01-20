"""
Experiment 3: Semantic Network Analysis

Research Question:
What are the thematic clusters in the narrative discourse?

Theoretical Grounding:
- Franco Moretti's network theory for literary analysis
- Social network analysis applied to texts
- Discourse analysis of entity-theme relations

Method:
1. Extract all dialogue from game data
2. Build co-occurrence matrix for entities and themes
3. Create network graph with weighted edges
4. Apply community detection (Louvain algorithm)
5. Visualize with force-directed layout
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict
from itertools import combinations

from .visualization import (
    create_figure, save_figure, add_source_annotation,
    save_table_markdown, save_table_csv,
    COLORS, get_community_color, setup_style
)
from .parsers import EventDumpParser, NarrativeExtractionParser, load_json_data, save_json_data


class SemanticNetwork:
    """
    Build and analyze semantic networks from game dialogue.
    
    Creates co-occurrence networks connecting characters (entities)
    and narrative concepts (themes) based on their presence in
    the same dialogue segments.
    
    Attributes:
        entities: List of entity keywords to track
        themes: List of theme keywords to track
        co_occurrence: Defaultdict of co-occurrence counts
        graph: NetworkX graph
        communities: Community partition dictionary
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize semantic network analyzer.
        
        Args:
            data_dir: Path to data directory
        """
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent / 'data'
        self.output_dir = Path(__file__).parent.parent / 'outputs'
        
        self.entities: List[str] = []
        self.themes: List[str] = []
        self.co_occurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        self.graph: Optional[nx.Graph] = None
        self.communities: Dict[str, int] = {}
        self.node_types: Dict[str, str] = {}  # 'entity' or 'theme'
        
    def load_keywords(self):
        """Load entity and theme keywords from context_keywords.json."""
        context_path = self.data_dir / 'context_keywords.json'
        context_data = load_json_data(str(context_path))
        
        self.entities = context_data.get('entities', [])
        self.themes = context_data.get('themes', [])
        
        # Build node type mapping
        for e in self.entities:
            self.node_types[e] = 'entity'
        for t in self.themes:
            self.node_types[t] = 'theme'
        
        print(f"Loaded {len(self.entities)} entities and {len(self.themes)} themes")
        
    def extract_dialogues(self) -> List[Dict[str, Any]]:
        """
        Extract all dialogue from EventTextDump.txt.
        
        Returns:
            List of dialogue dictionaries
        """
        parser = EventDumpParser()
        parser.parse_file(str(self.data_dir / 'EventTextDump.txt'))
        return parser.extract_all_dialogue()
    
    def process_dialogues(self, dialogues: List[Dict[str, Any]]):
        """
        Build co-occurrence matrix from all dialogue.
        
        Args:
            dialogues: List of dialogue dictionaries with 'text' field
        """
        self.co_occurrence = defaultdict(int)
        all_keywords = self.entities + self.themes
        
        for dialogue in dialogues:
            text = dialogue.get('text', '') or ''
            
            # Find all present keywords in this dialogue
            present = [kw for kw in all_keywords if kw in text]
            
            # Count co-occurrences (all pairs)
            for kw1, kw2 in combinations(present, 2):
                # Normalize pair ordering for consistency
                pair = tuple(sorted([kw1, kw2]))
                self.co_occurrence[pair] += 1
        
        print(f"Found {len(self.co_occurrence)} co-occurrence pairs")
        
    def build_network(self, threshold: int = 2) -> nx.Graph:
        """
        Create NetworkX graph from co-occurrences.
        
        Args:
            threshold: Minimum co-occurrence count to create edge
            
        Returns:
            NetworkX graph
        """
        self.graph = nx.Graph()
        
        # Add nodes
        for e in self.entities:
            self.graph.add_node(e, node_type='entity')
        for t in self.themes:
            self.graph.add_node(t, node_type='theme')
        
        # Add edges above threshold
        for (node1, node2), weight in self.co_occurrence.items():
            if weight >= threshold:
                self.graph.add_edge(node1, node2, weight=weight)
        
        # Remove isolated nodes
        isolated = list(nx.isolates(self.graph))
        self.graph.remove_nodes_from(isolated)
        
        print(f"Network: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        print(f"Removed {len(isolated)} isolated nodes")
        
        return self.graph
    
    def detect_communities(self) -> Dict[str, int]:
        """
        Apply community detection using Louvain algorithm.
        
        Returns:
            Dictionary mapping node names to community IDs
        """
        if self.graph is None or self.graph.number_of_nodes() == 0:
            self.communities = {}
            return self.communities
        
        try:
            # Try python-louvain package
            import community.community_louvain as community_louvain
            self.communities = community_louvain.best_partition(self.graph)
        except ImportError:
            try:
                # Fall back to networkx community detection
                from networkx.algorithms.community import greedy_modularity_communities
                communities_gen = greedy_modularity_communities(self.graph)
                self.communities = {}
                for idx, comm in enumerate(communities_gen):
                    for node in comm:
                        self.communities[node] = idx
            except Exception:
                # Final fallback: assign all to one community
                self.communities = {n: 0 for n in self.graph.nodes()}
        
        num_communities = len(set(self.communities.values()))
        print(f"Detected {num_communities} communities")
        
        return self.communities
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate network metrics.
        
        Returns:
            Dictionary of network statistics
        """
        if self.graph is None or self.graph.number_of_nodes() == 0:
            return {
                'num_nodes': 0,
                'num_edges': 0,
                'density': 0,
                'avg_clustering': 0,
                'avg_degree': 0,
                'num_communities': 0
            }
        
        G = self.graph
        
        # Basic metrics
        metrics = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': round(nx.density(G), 4),
            'num_communities': len(set(self.communities.values())) if self.communities else 0
        }
        
        # Clustering coefficient
        try:
            metrics['avg_clustering'] = round(nx.average_clustering(G), 4)
        except:
            metrics['avg_clustering'] = 0
        
        # Degree statistics
        degrees = dict(G.degree())
        if degrees:
            metrics['avg_degree'] = round(sum(degrees.values()) / len(degrees), 2)
            metrics['max_degree'] = max(degrees.values())
            metrics['max_degree_node'] = max(degrees, key=degrees.get)
        else:
            metrics['avg_degree'] = 0
            metrics['max_degree'] = 0
            metrics['max_degree_node'] = None
        
        # Centrality metrics
        if G.number_of_nodes() > 0:
            try:
                betweenness = nx.betweenness_centrality(G)
                top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
                metrics['top_betweenness'] = [{'node': n, 'score': round(s, 4)} for n, s in top_betweenness]
            except:
                metrics['top_betweenness'] = []
        
        # Node type breakdown
        entity_count = sum(1 for n in G.nodes() if self.node_types.get(n) == 'entity')
        theme_count = sum(1 for n in G.nodes() if self.node_types.get(n) == 'theme')
        metrics['entity_nodes'] = entity_count
        metrics['theme_nodes'] = theme_count
        
        # Top co-occurrences
        top_pairs = sorted(self.co_occurrence.items(), key=lambda x: x[1], reverse=True)[:20]
        metrics['top_co_occurrences'] = [
            {'pair': list(pair), 'count': count} 
            for pair, count in top_pairs
        ]
        
        # Community breakdown
        if self.communities:
            comm_sizes = defaultdict(int)
            for node, comm_id in self.communities.items():
                comm_sizes[comm_id] += 1
            metrics['community_sizes'] = dict(comm_sizes)
        
        return metrics
    
    def plot_network(self) -> plt.Figure:
        """
        Create force-directed network visualization.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.graph is None or self.graph.number_of_nodes() == 0:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.text(0.5, 0.5, 'No network data available', ha='center', va='center', fontsize=14)
            ax.axis('off')
            return fig
        
        G = self.graph
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Compute layout
        try:
            pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
        except:
            pos = nx.circular_layout(G)
        
        # Node colors by community
        if self.communities:
            node_colors = [get_community_color(self.communities.get(n, 0)) for n in G.nodes()]
        else:
            node_colors = [COLORS['entity'] if self.node_types.get(n) == 'entity' 
                          else COLORS['theme'] for n in G.nodes()]
        
        # Node sizes by degree
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees else 1
        node_sizes = [300 + 500 * (degrees[n] / max_degree) for n in G.nodes()]
        
        # Node shapes (circles for entities, different marker would need custom drawing)
        # For simplicity, we'll use different edge colors for entities vs themes
        
        # Draw edges
        edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
        max_weight = max(edge_weights) if edge_weights else 1
        edge_widths = [0.5 + 3 * (w / max_weight) for w in edge_weights]
        
        nx.draw_networkx_edges(G, pos, ax=ax,
                               width=edge_widths,
                               alpha=0.4,
                               edge_color='gray')
        
        # Draw entity nodes
        entity_nodes = [n for n in G.nodes() if self.node_types.get(n) == 'entity']
        entity_colors = [get_community_color(self.communities.get(n, 0)) if self.communities
                        else COLORS['entity'] for n in entity_nodes]
        entity_sizes = [node_sizes[list(G.nodes()).index(n)] for n in entity_nodes]
        
        nx.draw_networkx_nodes(G, pos, ax=ax,
                               nodelist=entity_nodes,
                               node_color=entity_colors,
                               node_size=entity_sizes,
                               node_shape='o',
                               alpha=0.9,
                               edgecolors='white',
                               linewidths=2)
        
        # Draw theme nodes
        theme_nodes = [n for n in G.nodes() if self.node_types.get(n) == 'theme']
        theme_colors = [get_community_color(self.communities.get(n, 0)) if self.communities
                       else COLORS['theme'] for n in theme_nodes]
        theme_sizes = [node_sizes[list(G.nodes()).index(n)] for n in theme_nodes]
        
        nx.draw_networkx_nodes(G, pos, ax=ax,
                               nodelist=theme_nodes,
                               node_color=theme_colors,
                               node_size=theme_sizes,
                               node_shape='s',  # Square for themes
                               alpha=0.9,
                               edgecolors='white',
                               linewidths=2)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, ax=ax,
                                font_size=9,
                                font_weight='bold')
        
        ax.set_title('Semantic Network: Entity-Theme Co-occurrence\n(Nodes colored by community)', 
                     fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
        
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                   markersize=12, label='Entity (Character/Faction)'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
                   markersize=12, label='Theme (Concept)'),
        ]
        
        # Add community colors if detected
        if self.communities:
            num_comm = len(set(self.communities.values()))
            for i in range(min(num_comm, 5)):
                legend_elements.append(
                    Patch(facecolor=get_community_color(i), label=f'Community {i+1}')
                )
        
        ax.legend(handles=legend_elements, loc='lower left', fontsize=9)
        
        plt.tight_layout()
        
        return fig
    
    def plot_co_occurrence_heatmap(self) -> plt.Figure:
        """
        Create heatmap of top co-occurrences.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        # Get top nodes by total co-occurrence
        node_totals = defaultdict(int)
        for (n1, n2), count in self.co_occurrence.items():
            node_totals[n1] += count
            node_totals[n2] += count
        
        top_nodes = sorted(node_totals.keys(), key=lambda x: node_totals[x], reverse=True)[:15]
        
        if len(top_nodes) < 2:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, 'Insufficient data for heatmap', ha='center', va='center')
            ax.axis('off')
            return fig
        
        # Build matrix
        n = len(top_nodes)
        matrix = np.zeros((n, n))
        
        for i, n1 in enumerate(top_nodes):
            for j, n2 in enumerate(top_nodes):
                if i != j:
                    pair = tuple(sorted([n1, n2]))
                    matrix[i, j] = self.co_occurrence.get(pair, 0)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create heatmap
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.set_xticklabels(top_nodes, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(top_nodes, fontsize=9)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Co-occurrence Count', fontsize=10)
        
        # Add value annotations
        for i in range(n):
            for j in range(n):
                if matrix[i, j] > 0:
                    text = ax.text(j, i, int(matrix[i, j]),
                                  ha='center', va='center', 
                                  color='white' if matrix[i, j] > matrix.max()/2 else 'black',
                                  fontsize=8)
        
        ax.set_title('Co-occurrence Heatmap: Top 15 Entities and Themes', 
                     fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    def plot_degree_distribution(self) -> plt.Figure:
        """
        Create degree distribution visualization.
        
        Returns:
            Matplotlib figure
        """
        setup_style()
        
        if self.graph is None or self.graph.number_of_nodes() == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No network data available', ha='center', va='center')
            ax.axis('off')
            return fig
        
        G = self.graph
        degrees = [d for n, d in G.degree()]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Histogram
        ax1.hist(degrees, bins=range(max(degrees)+2), color=COLORS['entity'], 
                 edgecolor='white', alpha=0.8, align='left')
        ax1.set_xlabel('Degree (Number of Connections)')
        ax1.set_ylabel('Number of Nodes')
        ax1.set_title('Degree Distribution', fontsize=12, fontweight='bold')
        
        # Top nodes by degree
        degree_dict = dict(G.degree())
        top_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        
        nodes = [n[0] for n in top_nodes]
        degs = [n[1] for n in top_nodes]
        colors = [COLORS['entity'] if self.node_types.get(n) == 'entity' else COLORS['theme'] for n in nodes]
        
        y_pos = np.arange(len(nodes))
        ax2.barh(y_pos, degs, color=colors, edgecolor='white')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(nodes, fontsize=9)
        ax2.set_xlabel('Degree')
        ax2.set_title('Top 10 Nodes by Degree', fontsize=12, fontweight='bold')
        ax2.invert_yaxis()
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['entity'], label='Entity'),
            Patch(facecolor=COLORS['theme'], label='Theme'),
        ]
        ax2.legend(handles=legend_elements, loc='lower right', fontsize=9)
        
        plt.tight_layout()
        
        return fig
    
    def run(self, beats=None) -> Dict[str, Any]:
        """
        Run complete semantic network analysis.
        
        Args:
            beats: Optional pre-parsed beats (unused, for interface compatibility)
            
        Returns:
            Dictionary with all results and file paths
        """
        print("="*60)
        print("EXPERIMENT 3: Semantic Network Analysis")
        print("="*60)
        
        # Load keywords
        print("\n[1/5] Loading keywords...")
        self.load_keywords()
        
        # Extract dialogues
        print("[2/5] Extracting dialogues from game data...")
        dialogues = self.extract_dialogues()
        print(f"  - Found {len(dialogues)} dialogue segments")
        
        # Build co-occurrence matrix
        print("[3/5] Building co-occurrence matrix...")
        self.process_dialogues(dialogues)
        
        # Build network
        print("[4/5] Building and analyzing network...")
        self.build_network(threshold=2)
        self.detect_communities()
        metrics = self.calculate_metrics()
        
        print(f"  - Network density: {metrics['density']}")
        print(f"  - Average clustering: {metrics['avg_clustering']}")
        print(f"  - Communities detected: {metrics['num_communities']}")
        
        # Generate visualizations
        print("[5/5] Generating visualizations...")
        
        # Figure 1: Network graph
        fig1 = self.plot_network()
        fig1_paths = save_figure(fig1, self.output_dir / 'figures' / 'exp3_semantic_network')
        plt.close(fig1)
        print(f"  - Saved: {fig1_paths}")
        
        # Figure 2: Co-occurrence heatmap
        fig2 = self.plot_co_occurrence_heatmap()
        fig2_paths = save_figure(fig2, self.output_dir / 'figures' / 'exp3_cooccurrence_heatmap')
        plt.close(fig2)
        print(f"  - Saved: {fig2_paths}")
        
        # Figure 3: Degree distribution
        fig3 = self.plot_degree_distribution()
        fig3_paths = save_figure(fig3, self.output_dir / 'figures' / 'exp3_degree_distribution')
        plt.close(fig3)
        print(f"  - Saved: {fig3_paths}")
        
        # Save tables and metrics
        print("  Saving tables and metrics...")
        
        # Top co-occurrences table
        top_pairs_data = []
        for pair, count in sorted(self.co_occurrence.items(), key=lambda x: x[1], reverse=True)[:20]:
            top_pairs_data.append({
                'Entity/Theme 1': pair[0],
                'Entity/Theme 2': pair[1],
                'Co-occurrence Count': count,
                'Type 1': self.node_types.get(pair[0], 'unknown'),
                'Type 2': self.node_types.get(pair[1], 'unknown')
            })
        
        if top_pairs_data:
            pairs_df = pd.DataFrame(top_pairs_data)
            md_path = save_table_markdown(pairs_df, 
                                           self.output_dir / 'tables' / 'exp3_cooccurrence_table.md',
                                           'Top Co-occurrence Pairs')
            csv_path = save_table_csv(pairs_df, self.output_dir / 'tables' / 'exp3_cooccurrence_table.csv')
            print(f"  - Saved: {md_path}")
            print(f"  - Saved: {csv_path}")
        else:
            md_path = csv_path = None
        
        # Metrics JSON
        metrics_path = self.output_dir / 'metrics' / 'exp3_network_metrics.json'
        save_json_data(metrics, str(metrics_path))
        print(f"  - Saved: {metrics_path}")
        
        print("\n✓ Experiment 3 complete!")
        
        return {
            'metrics': metrics,
            'figures': fig1_paths + fig2_paths + fig3_paths,
            'tables': [md_path, csv_path] if md_path else [],
            'metrics_file': str(metrics_path)
        }


if __name__ == '__main__':
    # Run experiment standalone
    exp = SemanticNetwork()
    results = exp.run()
    print("\nKey Metrics:")
    for key in ['num_nodes', 'num_edges', 'density', 'num_communities']:
        print(f"  {key}: {results['metrics'][key]}")
