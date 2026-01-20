"""
Data Parsers for Grim Fairy Tale Analysis

This module provides parsers for the two primary data sources:
1. EventTextDump.txt - Raw RPG Maker event dump (84,123 lines)
2. narrative_extraction.md - Structured narrative hierarchy

These parsers extract structured data suitable for computational humanities analysis.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import pandas as pd


class EventDumpParser:
    """
    Parser for raw EventTextDump.txt files from RPG Maker games.
    
    Extracts map metadata, event information, and command sequences
    for narrative density and structural analysis.
    
    Attributes:
        maps: List of parsed map dictionaries
        command_types: Mapping of raw command strings to normalized types
    """
    
    # Command type classification
    COMMAND_TYPES = {
        'Text': ['Text'],
        'Battle': ['Battle Processing'],
        'Logic': ['Conditional Branch', 'Control Switches', 'Control Variables', 
                  'Loop', 'Break Loop', 'Exit Event Processing', 'Script'],
        'Navigation': ['Transfer Player', 'Set Move Route', 'Wait for Move'],
        'Party': ['Change Party Member', 'Change Items', 'Change Gold'],
        'Audio': ['Play BGM', 'Play SE', 'Stop BGM', 'Change BGS'],
        'Visual': ['Change Transparent', 'Show Animation', 'Show Picture',
                   'Erase Picture', 'Screen Tone', 'Flash Screen', 'Shake Screen'],
        'Message': ['Show Choices', 'Input Number', 'Message Window'],
        'Common': ['Call Common Event'],
        'Wait': ['Wait'],
        'Other': []  # Fallback category
    }
    
    def __init__(self):
        """Initialize parser with empty map list."""
        self.maps: List[Dict[str, Any]] = []
        
    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Parse EventTextDump.txt into structured format.
        
        Args:
            filepath: Path to EventTextDump.txt
            
        Returns:
            List of map dictionaries containing:
            - id: Map ID number
            - name: Map name (Chinese)
            - events: List of event dictionaries with commands
        """
        self.maps = []
        current_map = None
        current_event = None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n\r')
                
                # Detect map headers: "Map ID: 001"
                if line.startswith("Map ID:"):
                    map_id = int(line.split(':')[1].strip())
                    current_map = {
                        'id': map_id,
                        'name': '',
                        'events': []
                    }
                    self.maps.append(current_map)
                    
                # Detect map names: "Map Name: 营地"
                elif line.startswith("Map Name:") and current_map is not None:
                    current_map['name'] = line.split(':', 1)[1].strip()
                    
                # Detect events: "Event ID: 006"
                elif line.startswith("Event ID:") and current_map is not None:
                    event_id = int(line.split(':')[1].strip())
                    current_event = {
                        'id': event_id,
                        'name': '',
                        'commands': []
                    }
                    current_map['events'].append(current_event)
                    
                # Detect event names
                elif line.startswith("Event Name:") and current_event is not None:
                    current_event['name'] = line.split(':', 1)[1].strip()
                    
                # Detect commands: "@>Text:", "@>Battle Processing:", etc.
                elif line.strip().startswith("@>") and current_event is not None:
                    cmd_type = self._extract_command_type(line)
                    content = self._extract_content(line)
                    current_event['commands'].append({
                        'type': cmd_type,
                        'normalized_type': self._normalize_type(cmd_type),
                        'line': line_num,
                        'content': content,
                        'raw': line.strip()
                    })
                    
                # Detect dialogue continuation lines
                elif line.strip().startswith(':    :') and current_event is not None:
                    if current_event['commands'] and current_event['commands'][-1]['type'] == 'Text':
                        # Append to previous text command's content
                        current_event['commands'][-1]['content'] += '\n' + line.strip()[6:].strip()
                        
        return self.maps
    
    def _extract_command_type(self, line: str) -> str:
        """
        Extract command type from @> line.
        
        Args:
            line: Raw line starting with @>
            
        Returns:
            Command type string (e.g., 'Text', 'Battle Processing')
        """
        # Pattern: @>CommandType: content or @>CommandType
        match = re.match(r'@>([^:]+)(?::|$)', line.strip())
        if match:
            return match.group(1).strip()
        return 'Unknown'
    
    def _extract_content(self, line: str) -> str:
        """
        Extract content after command type.
        
        Args:
            line: Raw line starting with @>
            
        Returns:
            Content string (may be empty)
        """
        # Find first colon after @> and extract content
        match = re.match(r'@>[^:]+:\s*(.*)', line.strip())
        if match:
            return match.group(1).strip()
        return ''
    
    def _normalize_type(self, cmd_type: str) -> str:
        """
        Normalize command type to category for analysis.
        
        Args:
            cmd_type: Raw command type string
            
        Returns:
            Normalized category (Text, Battle, Logic, Navigation, etc.)
        """
        for category, patterns in self.COMMAND_TYPES.items():
            if any(p in cmd_type for p in patterns):
                return category
        return 'Other'
    
    def count_commands_by_map(self) -> pd.DataFrame:
        """
        Count commands by type for each map.
        
        Returns:
            DataFrame with columns:
            - map_id, map_name
            - dialogue_count, battle_count, logic_count, navigation_count
            - total_commands, narrative_density, classification
        """
        data = []
        
        for m in self.maps:
            counts = defaultdict(int)
            
            for event in m['events']:
                for cmd in event['commands']:
                    counts[cmd['normalized_type']] += 1
            
            dialogue = counts.get('Text', 0)
            battle = counts.get('Battle', 0) + counts.get('Common', 0)  # Common events often trigger battles
            logic = counts.get('Logic', 0)
            navigation = counts.get('Navigation', 0)
            visual = counts.get('Visual', 0) + counts.get('Audio', 0)
            other = counts.get('Other', 0) + counts.get('Message', 0) + counts.get('Wait', 0) + counts.get('Party', 0)
            
            total = dialogue + battle + logic + navigation + visual + other
            density = dialogue / total if total > 0 else 0
            
            data.append({
                'map_id': m['id'],
                'map_name': m['name'],
                'dialogue_count': dialogue,
                'battle_count': battle,
                'logic_count': logic,
                'navigation_count': navigation,
                'visual_audio_count': visual,
                'other_count': other,
                'total_commands': total,
                'narrative_density': round(density, 4),
                'classification': self._classify_density(density)
            })
        
        return pd.DataFrame(data)
    
    def _classify_density(self, density: float) -> str:
        """
        Classify map by narrative density.
        
        Args:
            density: Narrative density value (0.0 to 1.0)
            
        Returns:
            Classification string
        """
        if density > 0.7:
            return 'Story-Heavy'
        elif density > 0.3:
            return 'Mixed'
        else:
            return 'Combat/Traversal'
    
    def extract_all_dialogue(self) -> List[Dict[str, Any]]:
        """
        Extract all dialogue text from parsed maps.
        
        Returns:
            List of dialogue dictionaries with map/event context
        """
        dialogues = []
        
        for m in self.maps:
            for event in m['events']:
                for cmd in event['commands']:
                    if cmd['normalized_type'] == 'Text':
                        dialogues.append({
                            'map_id': m['id'],
                            'map_name': m['name'],
                            'event_id': event['id'],
                            'event_name': event['name'],
                            'line': cmd['line'],
                            'text': cmd['content'],
                            'raw': cmd['raw']
                        })
        
        return dialogues
    
    def get_map_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for parsed maps.
        
        Returns:
            Dictionary with total maps, events, commands, etc.
        """
        total_events = sum(len(m['events']) for m in self.maps)
        total_commands = sum(
            len(cmd) 
            for m in self.maps 
            for e in m['events'] 
            for cmd in [e['commands']]
        )
        total_dialogue = sum(
            1 for m in self.maps 
            for e in m['events'] 
            for cmd in e['commands'] 
            if cmd['normalized_type'] == 'Text'
        )
        
        return {
            'total_maps': len(self.maps),
            'total_events': total_events,
            'total_commands': sum(len(e['commands']) for m in self.maps for e in m['events']),
            'total_dialogue_commands': total_dialogue,
            'maps_with_dialogue': sum(
                1 for m in self.maps 
                if any(cmd['normalized_type'] == 'Text' 
                       for e in m['events'] 
                       for cmd in e['commands'])
            )
        }


class NarrativeExtractionParser:
    """
    Parser for narrative_extraction.md structured narrative files.
    
    Extracts hierarchical narrative data organized as:
    Arc → Sequence → Beat with dialogue, speakers, and citations.
    
    Attributes:
        arcs: List of parsed arc dictionaries
        characters: Set of identified character names
        dialogues: List of all extracted dialogue entries
    """
    
    def __init__(self):
        """Initialize parser with empty data structures."""
        self.arcs: List[Dict[str, Any]] = []
        self.characters: set = set()
        self.dialogues: List[Dict[str, Any]] = []
        self.beats: List[Dict[str, Any]] = []
        
    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Parse narrative_extraction.md into structured format.
        
        Args:
            filepath: Path to narrative_extraction.md
            
        Returns:
            List of beat dictionaries with narrative context
        """
        self.arcs = []
        self.characters = set()
        self.dialogues = []
        self.beats = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse chapter/arc structure
        current_chapter = None
        current_arc = None
        current_sequence = None
        
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Chapter headers: "## CHAPTER 1: 小红帽"
            chapter_match = re.match(r'^## CHAPTER (\d+)[:：]?\s*(.+)?$', line)
            if chapter_match:
                current_chapter = chapter_match.group(1)
                i += 1
                continue
            
            # Arc headers: "### Arc 1.1: Camp Departure"
            arc_match = re.match(r'^### Arc (\d+\.\d+)[:：]?\s*(.+)?$', line)
            if arc_match:
                current_arc = arc_match.group(1)
                arc_name = arc_match.group(2) if arc_match.group(2) else ''
                self.arcs.append({
                    'chapter': current_chapter,
                    'arc_id': current_arc,
                    'name': arc_name,
                    'sequences': []
                })
                i += 1
                continue
            
            # Sequence headers: "#### Sequence 1.1.1: Awakening"
            seq_match = re.match(r'^#### Sequence (\d+\.\d+\.\d+)[:：]?\s*(.+)?$', line)
            if seq_match:
                current_sequence = seq_match.group(1)
                seq_name = seq_match.group(2) if seq_match.group(2) else ''
                
                # Parse sequence block
                sequence_data = self._parse_sequence_block(lines, i)
                if self.arcs:
                    self.arcs[-1]['sequences'].append({
                        'sequence_id': current_sequence,
                        'name': seq_name,
                        **sequence_data
                    })
                i += 1
                continue
            
            # Dialogue extraction: 「...」 with speaker
            dialogue_match = re.search(r'「(.+?)」', line)
            if dialogue_match:
                dialogue_text = dialogue_match.group(1)
                # Look for speaker on next line or same line
                speaker = self._extract_speaker(lines, i)
                
                self.dialogues.append({
                    'chapter': current_chapter,
                    'arc': current_arc,
                    'sequence': current_sequence,
                    'text': dialogue_text,
                    'speaker': speaker,
                    'line_num': i + 1
                })
                
                if speaker:
                    self.characters.add(speaker)
            
            # Beat extraction
            beat_match = re.match(r'^\d+\.\s*\*\*(.+?)\*\*', line)
            if beat_match:
                beat_desc = beat_match.group(1)
                self.beats.append({
                    'chapter': current_chapter,
                    'arc': current_arc,
                    'sequence': current_sequence,
                    'description': beat_desc,
                    'line_num': i + 1
                })
            
            i += 1
        
        return self.beats
    
    def _parse_sequence_block(self, lines: List[str], start_idx: int) -> Dict[str, Any]:
        """
        Parse a sequence block for location, source, and summary.
        
        Args:
            lines: All document lines
            start_idx: Starting index of sequence header
            
        Returns:
            Dictionary with location, source, summary data
        """
        result = {
            'location': None,
            'source_lines': None,
            'summary': '',
            'map_id': None,
            'event_id': None
        }
        
        i = start_idx + 1
        while i < len(lines) and not lines[i].startswith('####') and not lines[i].startswith('###'):
            line = lines[i]
            
            # Location: "**Location:** Map 001: 营地, Event 004"
            loc_match = re.search(r'\*\*Location:\*\*\s*(.+)', line)
            if loc_match:
                result['location'] = loc_match.group(1)
                # Extract map and event IDs
                map_match = re.search(r'Map (\d+)', result['location'])
                event_match = re.search(r'Event (\d+)', result['location'])
                if map_match:
                    result['map_id'] = int(map_match.group(1))
                if event_match:
                    result['event_id'] = int(event_match.group(1))
            
            # Source: "**Source:** Lines 143-158"
            source_match = re.search(r'\*\*Source:\*\*\s*Lines?\s*(\d+)(?:-(\d+))?', line)
            if source_match:
                start = int(source_match.group(1))
                end = int(source_match.group(2)) if source_match.group(2) else start
                result['source_lines'] = (start, end)
            
            # Summary section
            if line.strip() == '##### Summary':
                i += 1
                summary_lines = []
                while i < len(lines) and not lines[i].startswith('#'):
                    if lines[i].strip():
                        summary_lines.append(lines[i].strip())
                    i += 1
                result['summary'] = ' '.join(summary_lines)
                continue
            
            i += 1
        
        return result
    
    def _extract_speaker(self, lines: List[str], current_idx: int) -> Optional[str]:
        """
        Extract speaker from dialogue context.
        
        Args:
            lines: All document lines
            current_idx: Index of line with dialogue
            
        Returns:
            Speaker name or None
        """
        # Check next line for "— Speaker" pattern
        if current_idx + 1 < len(lines):
            next_line = lines[current_idx + 1]
            speaker_match = re.search(r'[—–-]\s*(.+)', next_line)
            if speaker_match:
                return speaker_match.group(1).strip()
        
        # Check same line for "Speaker：" before dialogue
        current_line = lines[current_idx]
        speaker_match = re.match(r'^>\s*(.+?)[:：]\s*$', current_line)
        if speaker_match:
            return speaker_match.group(1).strip()
        
        return None
    
    def get_dialogue_by_arc(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group dialogues by narrative arc.
        
        Returns:
            Dictionary mapping arc ID to list of dialogues
        """
        arc_dialogues = defaultdict(list)
        for d in self.dialogues:
            arc_key = d.get('arc', 'Unknown')
            arc_dialogues[arc_key].append(d)
        return dict(arc_dialogues)
    
    def get_character_appearances(self) -> pd.DataFrame:
        """
        Count character appearances across narrative.
        
        Returns:
            DataFrame with character, count, and arc distribution
        """
        char_counts = defaultdict(lambda: {'total': 0, 'arcs': set()})
        
        for d in self.dialogues:
            if d['speaker']:
                char_counts[d['speaker']]['total'] += 1
                if d['arc']:
                    char_counts[d['speaker']]['arcs'].add(d['arc'])
        
        data = [
            {
                'character': char,
                'dialogue_count': info['total'],
                'arc_count': len(info['arcs']),
                'arcs': ', '.join(sorted(info['arcs']))
            }
            for char, info in char_counts.items()
        ]
        
        return pd.DataFrame(data).sort_values('dialogue_count', ascending=False)
    
    def extract_all_text(self) -> str:
        """
        Extract all narrative text for text analysis.
        
        Returns:
            Concatenated text from all dialogues and summaries
        """
        texts = []
        
        for d in self.dialogues:
            texts.append(d['text'])
        
        for arc in self.arcs:
            for seq in arc.get('sequences', []):
                if seq.get('summary'):
                    texts.append(seq['summary'])
        
        return '\n'.join(texts)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for parsed narrative.
        
        Returns:
            Dictionary with counts of arcs, sequences, beats, dialogues
        """
        total_sequences = sum(len(a.get('sequences', [])) for a in self.arcs)
        
        return {
            'total_arcs': len(self.arcs),
            'total_sequences': total_sequences,
            'total_beats': len(self.beats),
            'total_dialogues': len(self.dialogues),
            'unique_characters': len(self.characters),
            'characters': sorted(self.characters)
        }


def load_json_data(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_data(data: Any, filepath: str) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        filepath: Output path
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Test parsing
    from pathlib import Path
    
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Test EventDumpParser
    print("Testing EventDumpParser...")
    dump_parser = EventDumpParser()
    maps = dump_parser.parse_file(data_dir / 'EventTextDump.txt')
    summary = dump_parser.get_map_summary()
    print(f"  Loaded {summary['total_maps']} maps")
    print(f"  Found {summary['total_dialogue_commands']} dialogue commands")
    
    # Test NarrativeExtractionParser
    print("\nTesting NarrativeExtractionParser...")
    narrative_parser = NarrativeExtractionParser()
    beats = narrative_parser.parse_file(data_dir / 'narrative_extraction.md')
    narrative_summary = narrative_parser.get_summary()
    print(f"  Loaded {narrative_summary['total_arcs']} arcs")
    print(f"  Found {narrative_summary['total_dialogues']} dialogues")
    print(f"  Identified {narrative_summary['unique_characters']} characters")
    
    print("\nParsing tests complete!")
