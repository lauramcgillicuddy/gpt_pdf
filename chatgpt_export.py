"""
ChatGPT Export Parser 💜✨
Handles parsing and exporting ChatGPT conversation data
"""

import json
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set
from io import BytesIO
import re
from collections import Counter

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class ChatGPTParser:
    """Parser for ChatGPT export files! 🌙"""

    def parse_zip(self, zip_path: str) -> List[Dict[str, Any]]:
        """
        Parse a ChatGPT export ZIP file.

        Args:
            zip_path: Path to the ZIP file

        Returns:
            List of conversation dictionaries
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Look for conversations.json
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('conversations.json'):
                    with zip_ref.open(file_info.filename) as f:
                        json_data = f.read().decode('utf-8')
                        return self.parse_json(json_data)

        raise FileNotFoundError("conversations.json not found in ZIP file")

    def parse_json(self, json_data: str) -> List[Dict[str, Any]]:
        """
        Parse ChatGPT conversations JSON data.

        Args:
            json_data: JSON string containing conversations

        Returns:
            List of parsed conversation dictionaries with extracted messages
        """
        raw_conversations = json.loads(json_data)
        parsed_conversations = []

        for convo in raw_conversations:
            parsed_convo = {
                'id': convo.get('id', ''),
                'title': convo.get('title', 'Untitled'),
                'create_time': convo.get('create_time', 0),
                'update_time': convo.get('update_time', 0),
                'messages': []
            }

            # Extract messages from the mapping structure
            mapping = convo.get('mapping', {})
            messages = self._extract_messages_from_mapping(mapping)
            parsed_convo['messages'] = messages

            parsed_conversations.append(parsed_convo)

        return parsed_conversations

    def _extract_messages_from_mapping(self, mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract linear message thread from ChatGPT's tree structure.

        Args:
            mapping: The conversation mapping from ChatGPT export

        Returns:
            List of message dictionaries in chronological order
        """
        if not mapping:
            return []

        # Build the tree structure
        nodes = {}
        root_id = None

        for node_id, node_data in mapping.items():
            nodes[node_id] = node_data
            if node_data.get('parent') is None:
                root_id = node_id

        if root_id is None:
            return []

        # Traverse tree to build message thread
        messages = []
        current_id = root_id

        while current_id:
            node = nodes.get(current_id)
            if not node:
                break

            # Extract message data if present
            message_data = node.get('message')
            if message_data:
                author = message_data.get('author', {})
                role = author.get('role', 'unknown')

                # Extract content
                content_data = message_data.get('content', {})
                if content_data:
                    parts = content_data.get('parts', [])
                    if parts:
                        content = '\n'.join(str(part) for part in parts if part)

                        messages.append({
                            'id': message_data.get('id', ''),
                            'role': role,
                            'content': content,
                            'create_time': message_data.get('create_time', 0)
                        })

            # Move to next child (follow first child in tree)
            children = node.get('children', [])
            current_id = children[0] if children else None

        return messages


# 🔍 ADVANCED SEARCH & ANALYSIS FUNCTIONS ✨

def detect_characters(conversation: Dict[str, Any], min_mentions: int = 3) -> List[Dict[str, Any]]:
    """
    Detect character names mentioned in a conversation! 💜

    Looks for capitalized words that appear multiple times (likely character names).

    Args:
        conversation: Conversation dictionary
        min_mentions: Minimum number of mentions to consider as a character

    Returns:
        List of character dicts with name and mention count
    """
    messages = conversation.get('messages', [])
    all_text = ' '.join(msg.get('content', '') for msg in messages)

    # Find capitalized words (potential names)
    # Matches words that start with capital letter, followed by lowercase
    # This catches "Harry" but not "THE" or "SHOUTING"
    potential_names = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', all_text)

    # Common words to exclude (not character names)
    common_words = {
        'The', 'This', 'That', 'These', 'Those', 'I', 'You', 'He', 'She', 'It',
        'We', 'They', 'What', 'When', 'Where', 'Why', 'How', 'Who', 'Which',
        'Yes', 'No', 'Maybe', 'Please', 'Thanks', 'Hello', 'Hi', 'Bye',
        'Today', 'Tomorrow', 'Yesterday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday', 'January', 'February',
        'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December', 'ChatGPT', 'OpenAI'
    }

    # Count occurrences
    name_counts = Counter(potential_names)

    # Filter and format results
    characters = []
    for name, count in name_counts.most_common():
        if count >= min_mentions and name not in common_words and len(name) > 1:
            characters.append({
                'name': name,
                'mentions': count
            })

    return characters


def detect_themes(conversation: Dict[str, Any]) -> List[str]:
    """
    Detect content themes/tags in a conversation! 🌙

    Looks for keywords that indicate themes like fluff, romance, angst, etc.

    Args:
        conversation: Conversation dictionary

    Returns:
        List of detected theme tags
    """
    messages = conversation.get('messages', [])
    all_text = ' '.join(msg.get('content', '') for msg in messages).lower()

    # Theme keyword mappings with adorable pastel goth vibes! 💜
    theme_keywords = {
        '💕 Romance': [
            'love', 'kiss', 'romance', 'romantic', 'dating', 'boyfriend', 'girlfriend',
            'crush', 'flirt', 'heart', 'affection', 'valentine', 'date night', 'sweetheart'
        ],
        '✨ Fluff': [
            'cute', 'adorable', 'sweet', 'wholesome', 'cozy', 'comfort', 'warm',
            'snuggle', 'cuddle', 'soft', 'gentle', 'tender', 'precious', 'fluffy'
        ],
        '🔥 Explicit': [
            'nsfw', 'explicit', 'mature', 'adult', 'sexual', 'intimate', 'rated',
            'smut', 'lemon', '18+'
        ],
        '😢 Angst': [
            'angst', 'sad', 'cry', 'tears', 'pain', 'hurt', 'suffer', 'tragic',
            'heartbreak', 'sorrow', 'grief', 'anguish', 'despair', 'melancholy'
        ],
        '😱 Horror/Fear': [
            'horror', 'fear', 'scary', 'terror', 'afraid', 'frightened', 'nightmare',
            'creepy', 'eerie', 'spooky', 'haunted', 'dark', 'sinister', 'dread'
        ],
        '⚔️ Action': [
            'fight', 'battle', 'combat', 'action', 'war', 'attack', 'sword',
            'weapon', 'explosion', 'chase', 'duel', 'violence'
        ],
        '😂 Humor': [
            'funny', 'hilarious', 'comedy', 'joke', 'laugh', 'humor', 'amusing',
            'silly', 'goofy', 'witty', 'sarcasm', 'parody'
        ],
        '🎭 Drama': [
            'drama', 'conflict', 'tension', 'intense', 'emotional', 'dramatic',
            'confrontation', 'argument', 'dispute'
        ],
        '🔮 Fantasy': [
            'magic', 'fantasy', 'wizard', 'witch', 'spell', 'enchant', 'dragon',
            'elf', 'dwarf', 'fairy', 'mythical', 'supernatural', 'mystical'
        ],
        '🚀 Sci-Fi': [
            'space', 'alien', 'robot', 'future', 'technology', 'cyber', 'ai',
            'spacecraft', 'galaxy', 'planet', 'science fiction'
        ],
        '🌸 Slice of Life': [
            'everyday', 'daily', 'ordinary', 'routine', 'casual', 'mundane',
            'realistic', 'contemporary', 'normal life'
        ],
        '🎨 Creative Writing': [
            'story', 'narrative', 'plot', 'character', 'fiction', 'writing',
            'novel', 'fanfic', 'fanfiction', 'creative', 'roleplay', 'rp'
        ]
    }

    detected_themes = []

    for theme, keywords in theme_keywords.items():
        # Count how many keywords from this theme appear
        matches = sum(1 for keyword in keywords if keyword in all_text)

        # If enough keywords match, add the theme
        threshold = max(1, len(keywords) // 5)  # At least 20% of keywords
        if matches >= threshold:
            detected_themes.append(theme)

    return detected_themes


def search_conversations(
    conversations: List[Dict[str, Any]],
    query: str,
    search_content: bool = True,
    search_titles: bool = True
) -> List[Dict[str, Any]]:
    """
    Advanced search through conversations! 🔍✨

    Searches both titles and message content for the query.

    Args:
        conversations: List of conversation dictionaries
        query: Search query string
        search_content: Whether to search in message content
        search_titles: Whether to search in titles

    Returns:
        List of matching conversations
    """
    if not query:
        return conversations

    query_lower = query.lower()
    results = []

    for convo in conversations:
        match = False

        # Search in title
        if search_titles:
            title = convo.get('title', '').lower()
            if query_lower in title:
                match = True

        # Search in content
        if search_content and not match:
            messages = convo.get('messages', [])
            for msg in messages:
                content = msg.get('content', '').lower()
                if query_lower in content:
                    match = True
                    break

        if match:
            results.append(convo)

    return results


def filter_by_themes(conversations: List[Dict[str, Any]], themes: List[str]) -> List[Dict[str, Any]]:
    """
    Filter conversations by detected themes! 🎨

    Args:
        conversations: List of conversation dictionaries
        themes: List of theme tags to filter by

    Returns:
        Conversations that contain any of the specified themes
    """
    if not themes:
        return conversations

    results = []

    for convo in conversations:
        convo_themes = detect_themes(convo)
        # Check if any of the requested themes are in this conversation
        if any(theme in convo_themes for theme in themes):
            results.append(convo)

    return results


def filter_by_characters(
    conversations: List[Dict[str, Any]],
    character_names: List[str]
) -> List[Dict[str, Any]]:
    """
    Filter conversations by character names! 💜

    Args:
        conversations: List of conversation dictionaries
        character_names: List of character names to search for

    Returns:
        Conversations that mention any of the specified characters
    """
    if not character_names:
        return conversations

    results = []

    for convo in conversations:
        characters = detect_characters(convo, min_mentions=2)
        detected_names = [c['name'].lower() for c in characters]

        # Check if any requested character is in this conversation
        if any(char.lower() in detected_names for char in character_names):
            results.append(convo)

    return results


def export_to_word(conversation: Dict[str, Any]) -> BytesIO:
    """
    Export conversation to Word document with pastel goth styling! 💜

    Args:
        conversation: Conversation dictionary

    Returns:
        BytesIO containing the Word document
    """
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx is required for Word export")

    doc = Document()

    # Title with styling
    title = doc.add_heading(conversation.get('title', 'Untitled Conversation'), 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.color.rgb = RGBColor(183, 148, 201)  # Pastel purple

    # Metadata
    create_time = datetime.fromtimestamp(conversation.get('create_time', 0))
    metadata = doc.add_paragraph()
    metadata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = metadata.add_run(f"Created: {create_time.strftime('%B %d, %Y at %I:%M %p')}")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(201, 163, 216)

    doc.add_paragraph()  # Spacing

    # Add messages
    messages = conversation.get('messages', [])
    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        timestamp = datetime.fromtimestamp(msg.get('create_time', 0))

        # Role header with color
        role_para = doc.add_paragraph()
        role_run = role_para.add_run(f"{role.upper()} • {timestamp.strftime('%I:%M %p')}")
        role_run.bold = True

        if role == 'user':
            role_run.font.color.rgb = RGBColor(180, 212, 240)  # Pastel blue
        elif role == 'assistant':
            role_run.font.color.rgb = RGBColor(201, 240, 180)  # Pastel green
        else:
            role_run.font.color.rgb = RGBColor(232, 180, 240)  # Pastel purple

        # Message content
        content_para = doc.add_paragraph(content)
        content_para.paragraph_format.left_indent = Inches(0.25)

        # Add spacing
        doc.add_paragraph()

    # Save to BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def export_to_pdf(conversation: Dict[str, Any]) -> BytesIO:
    """
    Export conversation to PDF with pastel goth styling! 🌙

    Args:
        conversation: Conversation dictionary

    Returns:
        BytesIO containing the PDF
    """
    if not PDF_AVAILABLE:
        raise ImportError("reportlab is required for PDF export")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Styles
    styles = getSampleStyleSheet()

    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#b794c9'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Custom metadata style
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#c9a3d8'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # User message style
    user_style = ParagraphStyle(
        'UserStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#b4d4f0'),
        spaceAfter=5
    )

    # Assistant message style
    assistant_style = ParagraphStyle(
        'AssistantStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#c9f0b4'),
        spaceAfter=5
    )

    # Content style
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#e8b4f0'),
        leftIndent=20,
        spaceAfter=15
    )

    # Add title
    title = conversation.get('title', 'Untitled Conversation')
    story.append(Paragraph(title, title_style))

    # Add metadata
    create_time = datetime.fromtimestamp(conversation.get('create_time', 0))
    meta_text = f"Created: {create_time.strftime('%B %d, %Y at %I:%M %p')}"
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 0.3 * inch))

    # Add messages
    messages = conversation.get('messages', [])
    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '').replace('<', '&lt;').replace('>', '&gt;')
        timestamp = datetime.fromtimestamp(msg.get('create_time', 0))

        # Role header
        role_text = f"<b>{role.upper()}</b> • {timestamp.strftime('%I:%M %p')}"

        if role == 'user':
            story.append(Paragraph(role_text, user_style))
        elif role == 'assistant':
            story.append(Paragraph(role_text, assistant_style))
        else:
            story.append(Paragraph(role_text, content_style))

        # Content
        story.append(Paragraph(content, content_style))
        story.append(Spacer(1, 0.2 * inch))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def get_conversation_stats(conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get statistics about conversations.

    Args:
        conversations: List of conversation dictionaries

    Returns:
        Dictionary with stats
    """
    total_conversations = len(conversations)
    total_messages = sum(len(c.get('messages', [])) for c in conversations)

    oldest = None
    newest = None

    for convo in conversations:
        create_time = convo.get('create_time', 0)
        if oldest is None or create_time < oldest:
            oldest = create_time
        if newest is None or create_time > newest:
            newest = create_time

    return {
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'oldest_conversation': datetime.fromtimestamp(oldest) if oldest else None,
        'newest_conversation': datetime.fromtimestamp(newest) if newest else None,
        'average_messages_per_conversation': total_messages / total_conversations if total_conversations > 0 else 0
    }
