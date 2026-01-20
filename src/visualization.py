"""
Visualization Utilities for Grim Fairy Tale Analysis

This module provides shared plotting utilities, style configuration,
and helper functions for creating publication-quality figures.

All figures follow DH publication standards:
- 300 DPI PNG for raster output
- PDF for vector output
- Chinese text support via DejaVu Sans/Noto Sans CJK
- Colorblind-friendly palettes
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# ============================================================================
# STYLE CONFIGURATION
# ============================================================================

# Color palette (colorblind-friendly)
COLORS = {
    # Narrative density classification
    'story': '#E74C3C',       # Red - Story-heavy maps
    'mixed': '#F39C12',       # Orange - Mixed content
    'combat': '#3498DB',      # Blue - Combat/traversal
    
    # Motif context colors
    'innocence': '#FFB6C1',   # Light pink
    'military': '#4169E1',    # Royal blue
    'posthuman': '#8B0000',   # Dark red
    'neutral': '#808080',     # Gray
    
    # Network colors
    'entity': '#2ECC71',      # Green - Entity nodes
    'theme': '#9B59B6',       # Purple - Theme nodes
    
    # Alignment colors
    'direct': '#3498DB',      # Blue - Direct transposition
    'structural': '#F39C12',  # Orange - Structural homology
    
    # Community colors (for network analysis)
    'community_1': '#E74C3C',
    'community_2': '#3498DB',
    'community_3': '#2ECC71',
    'community_4': '#9B59B6',
    'community_5': '#F39C12',
}

# Figure sizes (in inches)
FIGURE_SIZES = {
    'single': (8, 6),         # Single column
    'double': (10, 6),        # Double column
    'square': (10, 10),       # Square (networks)
    'tall': (12, 20),         # Tall (heatmaps)
    'wide': (14, 6),          # Wide (timelines)
}


def setup_style():
    """
    Configure matplotlib and seaborn for publication-quality figures.
    
    Sets up:
    - Seaborn whitegrid style
    - Chinese-compatible fonts
    - Default figure parameters
    """
    # Set seaborn style
    sns.set_style("whitegrid")
    
    # Configure font handling for Chinese characters
    # Try multiple font options in order of preference
    font_candidates = [
        'WenQuanYi Zen Hei',      # Most commonly available CJK font
        'Noto Sans CJK SC',
        'Noto Sans CJK JP',        # JP version also supports Chinese
        'Noto Sans CJK',
        'Source Han Sans SC',
        'WenQuanYi Micro Hei',
        'Arial Unicode MS',
        'DejaVu Sans',
    ]
    
    # Find available fonts
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    selected_font = 'DejaVu Sans'  # Fallback
    for font in font_candidates:
        if font in available_fonts:
            selected_font = font
            break
    
    # Apply matplotlib settings
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [selected_font, 'DejaVu Sans', 'Arial'],
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 100,  # Display DPI
        'savefig.dpi': 300,  # Save DPI
        'axes.unicode_minus': False,
    })
    
    return selected_font


def get_chinese_font():
    """
    Get a font path that supports Chinese characters.
    
    Returns:
        Path to a Chinese-compatible font file, or None
    """
    # Common Chinese font paths
    font_paths = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    ]
    
    for path in font_paths:
        if Path(path).exists():
            return path
    
    return None


# ============================================================================
# FIGURE CREATION UTILITIES
# ============================================================================

def create_figure(size_key: str = 'double', 
                  title: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a new figure with standard sizing.
    
    Args:
        size_key: Key from FIGURE_SIZES ('single', 'double', 'square', 'tall', 'wide')
        title: Optional figure title
        
    Returns:
        Tuple of (figure, axes)
    """
    setup_style()
    
    size = FIGURE_SIZES.get(size_key, FIGURE_SIZES['double'])
    fig, ax = plt.subplots(figsize=size)
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold')
    
    return fig, ax


def create_subplots(nrows: int, ncols: int, 
                    size_key: str = 'double',
                    title: Optional[str] = None) -> Tuple[plt.Figure, np.ndarray]:
    """
    Create a figure with subplots.
    
    Args:
        nrows: Number of rows
        ncols: Number of columns
        size_key: Base size key (will be scaled)
        title: Optional figure title
        
    Returns:
        Tuple of (figure, axes array)
    """
    setup_style()
    
    base_size = FIGURE_SIZES.get(size_key, FIGURE_SIZES['double'])
    fig_width = base_size[0] * ncols * 0.6
    fig_height = base_size[1] * nrows * 0.6
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(fig_width, fig_height))
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold')
    
    return fig, axes


def save_figure(fig: plt.Figure, 
                output_path: str, 
                formats: List[str] = ['png', 'pdf']) -> List[str]:
    """
    Save figure in multiple formats.
    
    Args:
        fig: Matplotlib figure
        output_path: Base output path (without extension)
        formats: List of formats to save ('png', 'pdf')
        
    Returns:
        List of saved file paths
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    saved_paths = []
    
    for fmt in formats:
        filepath = output_path.with_suffix(f'.{fmt}')
        
        dpi = 300 if fmt == 'png' else None
        fig.savefig(filepath, 
                    dpi=dpi, 
                    bbox_inches='tight',
                    facecolor='white',
                    edgecolor='none')
        saved_paths.append(str(filepath))
    
    return saved_paths


def add_source_annotation(ax: plt.Axes, 
                          source_text: str = "Source: EventTextDump.txt analysis"):
    """
    Add source annotation to figure.
    
    Args:
        ax: Matplotlib axes
        source_text: Source attribution text
    """
    ax.annotate(source_text, 
                xy=(1.0, -0.12), 
                xycoords='axes fraction',
                fontsize=8, 
                color='gray',
                ha='right')


# ============================================================================
# SPECIFIC VISUALIZATION FUNCTIONS
# ============================================================================

def plot_horizontal_bar_chart(data: Dict[str, float],
                               title: str,
                               xlabel: str,
                               ylabel: str,
                               color_map: Optional[Dict[str, str]] = None,
                               ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Create a horizontal bar chart.
    
    Args:
        data: Dictionary mapping labels to values
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color_map: Optional mapping of labels to colors
        ax: Optional axes to plot on
        
    Returns:
        Matplotlib axes
    """
    if ax is None:
        fig, ax = create_figure('double')
    
    labels = list(data.keys())
    values = list(data.values())
    
    if color_map:
        colors = [color_map.get(label, COLORS['mixed']) for label in labels]
    else:
        colors = [COLORS['mixed']] * len(labels)
    
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, values, color=colors, edgecolor='white', linewidth=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Add value labels
    for i, v in enumerate(values):
        ax.text(v + 0.01, i, f'{v:.2f}', va='center', fontsize=9)
    
    ax.invert_yaxis()  # Highest values at top
    
    return ax


def plot_stacked_area(df, x_col: str, value_cols: List[str],
                       colors: List[str],
                       title: str,
                       xlabel: str = '',
                       ylabel: str = 'Percentage (%)',
                       ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Create a stacked area chart.
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        value_cols: List of column names for stacked values
        colors: List of colors for each value column
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        ax: Optional axes to plot on
        
    Returns:
        Matplotlib axes
    """
    if ax is None:
        fig, ax = create_figure('double')
    
    x = df[x_col]
    y_stack = [df[col].values for col in value_cols]
    
    ax.stackplot(x, *y_stack, labels=value_cols, colors=colors, alpha=0.8)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_ylim(0, 100)
    
    return ax


def plot_network_graph(G, 
                        node_colors: Dict[str, str],
                        node_sizes: Dict[str, float],
                        title: str,
                        layout: str = 'spring',
                        ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Plot a network graph with customized styling.
    
    Args:
        G: NetworkX graph
        node_colors: Mapping of node names to colors
        node_sizes: Mapping of node names to sizes
        title: Chart title
        layout: Layout algorithm ('spring', 'kamada_kawai', 'circular')
        ax: Optional axes to plot on
        
    Returns:
        Matplotlib axes
    """
    import networkx as nx
    
    if ax is None:
        fig, ax = create_figure('square')
    
    # Compute layout
    if layout == 'spring':
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.circular_layout(G)
    
    # Prepare node attributes
    colors = [node_colors.get(n, COLORS['mixed']) for n in G.nodes()]
    sizes = [node_sizes.get(n, 300) for n in G.nodes()]
    
    # Draw edges
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    edge_widths = [2 * w / max_weight for w in edge_weights]
    
    nx.draw_networkx_edges(G, pos, ax=ax, 
                           width=edge_widths, 
                           alpha=0.5, 
                           edge_color='gray')
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_color=colors,
                           node_size=sizes,
                           alpha=0.9,
                           edgecolors='white',
                           linewidths=2)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax,
                            font_size=9,
                            font_weight='bold')
    
    ax.set_title(title)
    ax.axis('off')
    
    return ax


def create_heatmap(data: np.ndarray,
                   row_labels: List[str],
                   col_labels: List[str],
                   title: str,
                   cmap: str = 'YlOrRd',
                   ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Create a heatmap visualization.
    
    Args:
        data: 2D numpy array of values
        row_labels: Labels for rows
        col_labels: Labels for columns
        title: Chart title
        cmap: Colormap name
        ax: Optional axes to plot on
        
    Returns:
        Matplotlib axes
    """
    if ax is None:
        fig, ax = create_figure('square')
    
    im = ax.imshow(data, cmap=cmap, aspect='auto')
    
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, rotation=45, ha='right')
    ax.set_yticklabels(row_labels)
    
    ax.set_title(title)
    
    # Add colorbar
    plt.colorbar(im, ax=ax, shrink=0.8)
    
    return ax


def get_classification_color(classification: str) -> str:
    """
    Get color for density classification.
    
    Args:
        classification: 'Story-Heavy', 'Mixed', or 'Combat/Traversal'
        
    Returns:
        Color hex code
    """
    mapping = {
        'Story-Heavy': COLORS['story'],
        'Mixed': COLORS['mixed'],
        'Combat/Traversal': COLORS['combat'],
    }
    return mapping.get(classification, COLORS['mixed'])


def get_context_color(context: str) -> str:
    """
    Get color for motif context.
    
    Args:
        context: 'innocence', 'military', 'posthuman', or 'neutral'
        
    Returns:
        Color hex code
    """
    return COLORS.get(context, COLORS['neutral'])


def get_community_color(community_id: int) -> str:
    """
    Get color for network community.
    
    Args:
        community_id: Community index (0-based)
        
    Returns:
        Color hex code
    """
    community_colors = [
        COLORS['community_1'],
        COLORS['community_2'],
        COLORS['community_3'],
        COLORS['community_4'],
        COLORS['community_5'],
    ]
    return community_colors[community_id % len(community_colors)]


# ============================================================================
# TABLE GENERATION
# ============================================================================

def save_table_markdown(df, filepath: str, title: Optional[str] = None) -> str:
    """
    Save DataFrame as markdown table.
    
    Args:
        df: DataFrame to save
        filepath: Output path
        title: Optional table title
        
    Returns:
        Path to saved file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if title:
            f.write(f'# {title}\n\n')
        f.write(df.to_markdown(index=False))
        f.write('\n')
    
    return str(filepath)


def save_table_csv(df, filepath: str) -> str:
    """
    Save DataFrame as CSV.
    
    Args:
        df: DataFrame to save
        filepath: Output path
        
    Returns:
        Path to saved file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    return str(filepath)


# Initialize style on import
_font = setup_style()
print(f"Visualization module loaded. Using font: {_font}")
