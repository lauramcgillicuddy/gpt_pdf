"""
ChatGPT Export Parser 💜✨
Handles parsing and exporting ChatGPT conversation data
"""

import json
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from io import BytesIO

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
