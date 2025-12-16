import streamlit as st
import json
import zipfile
from pathlib import Path
from datetime import datetime
from io import BytesIO
import tempfile

# Import our ChatGPT parser and advanced search functions
from chatgpt_export import (
    ChatGPTParser, export_to_word, export_to_pdf,
    search_conversations, detect_themes, detect_characters,
    filter_by_themes, filter_by_characters, analyze_character_gallery
)

# 🌙✨ PASTEL GOTH AESTHETIC ✨🌙
def load_custom_css():
    """Load our adorable pastel goth styling! 💜🖤"""
    st.markdown("""
        <style>
        /* Main background - soft dark with purple tint */
        .stApp {
            background: linear-gradient(135deg, #1a0a1e 0%, #2d1b3d 50%, #1a0a1e 100%);
            font-family: 'Georgia', serif;
        }

        /* Headers with pastel goth vibes */
        h1, h2, h3 {
            background: linear-gradient(90deg, #e8b4f0 0%, #c9a3d8 50%, #b794c9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(232, 180, 240, 0.3);
            font-family: 'Georgia', serif;
            letter-spacing: 2px;
        }

        /* Cute decorative borders with lace effect */
        .element-container {
            border-image: linear-gradient(45deg, #e8b4f0, #c9a3d8) 1;
        }

        /* File uploader styling */
        .stFileUploader {
            background: linear-gradient(135deg, #2d1b3d 0%, #3d2548 100%);
            border: 2px solid #e8b4f0;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(232, 180, 240, 0.2);
        }

        .stFileUploader label {
            color: #e8b4f0 !important;
            font-size: 18px;
            font-weight: bold;
        }

        /* Buttons - pastel goth style */
        .stButton button {
            background: linear-gradient(135deg, #b794c9 0%, #9b7bb5 100%);
            color: white;
            border: 2px solid #e8b4f0;
            border-radius: 25px;
            padding: 10px 25px;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(232, 180, 240, 0.3);
        }

        .stButton button:hover {
            background: linear-gradient(135deg, #e8b4f0 0%, #c9a3d8 100%);
            box-shadow: 0 0 25px rgba(232, 180, 240, 0.6);
            transform: translateY(-2px);
        }

        /* Text inputs and search bars */
        .stTextInput input {
            background: #2d1b3d;
            color: #e8b4f0;
            border: 2px solid #b794c9;
            border-radius: 10px;
            padding: 10px;
        }

        .stTextInput input:focus {
            border-color: #e8b4f0;
            box-shadow: 0 0 15px rgba(232, 180, 240, 0.4);
        }

        /* Select boxes */
        .stSelectbox select {
            background: #2d1b3d;
            color: #e8b4f0;
            border: 2px solid #b794c9;
            border-radius: 10px;
        }

        /* Expanders - conversation cards */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #2d1b3d 0%, #3d2548 100%);
            border: 2px solid #e8b4f0;
            border-radius: 15px;
            color: #e8b4f0 !important;
            font-weight: bold;
            box-shadow: 0 0 15px rgba(232, 180, 240, 0.2);
        }

        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #3d2548 0%, #4d3558 100%);
            box-shadow: 0 0 25px rgba(232, 180, 240, 0.4);
        }

        /* Message containers */
        .stMarkdown {
            color: #e8b4f0;
        }

        /* Decorative dividers */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #e8b4f0, transparent);
            margin: 30px 0;
        }

        /* Info/success/error boxes */
        .stAlert {
            background: #2d1b3d;
            border: 2px solid #e8b4f0;
            border-radius: 10px;
            color: #e8b4f0;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a0a1e 0%, #2d1b3d 100%);
        }

        /* Custom card styling for conversations */
        .convo-card {
            background: linear-gradient(135deg, #2d1b3d 0%, #3d2548 100%);
            border: 2px solid #e8b4f0;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 0 20px rgba(232, 180, 240, 0.2);
            transition: all 0.3s ease;
        }

        .convo-card:hover {
            box-shadow: 0 0 30px rgba(232, 180, 240, 0.4);
            transform: translateY(-3px);
        }

        /* Lace-like decorative elements */
        .lace-divider {
            width: 100%;
            height: 20px;
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                #e8b4f0 10px,
                #e8b4f0 11px
            );
            opacity: 0.3;
            margin: 20px 0;
        }

        /* Sparkle effect on hover */
        @keyframes sparkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        .sparkle {
            animation: sparkle 2s ease-in-out infinite;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main app - ChatGPT Export Parser with Pastel Goth Vibes! 💜✨"""

    # Set page config
    st.set_page_config(
        page_title="💜 ChatGPT Export Parser ✨",
        page_icon="🌙",
        layout="wide"
    )

    # Load our cute styling
    load_custom_css()

    # Header with adorable decorations
    st.markdown("<h1 style='text-align: center;'>🌙✨ ChatGPT Export Parser ✨🌙</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e8b4f0; font-size: 18px;'>~ A pastel goth dream for your ChatGPT conversations ~</p>", unsafe_allow_html=True)
    st.markdown("<div class='lace-divider'></div>", unsafe_allow_html=True)

    # Sidebar with navigation and rogue's gallery
    with st.sidebar:
        st.markdown("### 🦇 Navigation 🦇")
        page = st.radio(
            "",
            ["💬 Upload & Browse", "📊 About"],
            label_visibility="collapsed"
        )

        # Show Rogue's Gallery if we have conversations loaded
        if 'character_gallery' in st.session_state and st.session_state.character_gallery:
            st.markdown("---")
            st.markdown("### 🎭 Rogue's Gallery 🎭")
            st.markdown("<p style='font-size: 12px; color: #c9a3d8;'>Click a character to filter threads!</p>", unsafe_allow_html=True)

            gallery = st.session_state.character_gallery

            # Show top characters
            for char in gallery[:10]:  # Top 10 characters
                with st.expander(f"🦇 {char['name']}"):
                    st.markdown(f"**Threads:** {char['thread_count']}")
                    st.markdown(f"**Total mentions:** {char['total_mentions']}")

                    if char['dominant_themes']:
                        st.markdown("**Themes:**")
                        for theme in char['dominant_themes']:
                            count = char['theme_counts'].get(theme, 0)
                            st.markdown(f"- {theme} ({count})")

                    # Filter button
                    if st.button(f"📖 Show {char['name']}'s threads", key=f"gallery_{char['name']}"):
                        st.session_state['filter_character'] = char['name']
                        st.rerun()

    if page == "💬 Upload & Browse":
        show_upload_page()
    else:
        show_about_page()

def show_upload_page():
    """Upload and browse ChatGPT exports! 💜"""

    st.markdown("## 💜 Upload Your ChatGPT Export")

    # Instructions with cute styling
    with st.expander("✨ How to Get Your ChatGPT Export ✨"):
        st.markdown("""
        1. Go to ChatGPT → Settings ⚙️
        2. Click on **Data controls**
        3. Select **Export data**
        4. Wait for the email with your export 📧
        5. Upload the ZIP file here! 💜

        You can upload either:
        - 📦 The full ZIP file from ChatGPT
        - 📄 Just the `conversations.json` file
        """)

    st.markdown("<div class='lace-divider'></div>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "🌙 Drop your export here 🌙",
        type=["zip", "json"],
        help="Upload your ChatGPT export (ZIP or JSON)"
    )

    if uploaded_file is not None:
        try:
            # Parse the file
            parser = ChatGPTParser()
            conversations = None

            if uploaded_file.name.endswith('.zip'):
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = Path(tmpdir) / "export.zip"
                    zip_path.write_bytes(uploaded_file.getvalue())
                    conversations = parser.parse_zip(str(zip_path))
            else:
                conversations = parser.parse_json(uploaded_file.getvalue().decode('utf-8'))

            if conversations:
                st.success(f"✨ Found {len(conversations)} conversations! ✨")

                # Generate character gallery for sidebar
                st.session_state['character_gallery'] = analyze_character_gallery(conversations)
                st.session_state['all_conversations'] = conversations

                show_conversations(conversations)
            else:
                st.warning("No conversations found in the export 🥺")

        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)} 💔")

def show_conversations(conversations):
    """Display conversations with advanced search and filters! 💜✨"""

    st.markdown("<div class='lace-divider'></div>", unsafe_allow_html=True)
    st.markdown("## 🔮 Your Conversations 🔮")

    # Advanced search section
    st.markdown("### 🔍 Search & Filter")

    # Search row
    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input(
            "💬 Search text",
            placeholder="Search in titles and content...",
            help="Searches both conversation titles and message content!"
        )

    with col2:
        search_in_content = st.checkbox("🔍 Search in messages", value=True, help="Search within message content (not just titles)")

    # Advanced filters row
    st.markdown("#### ✨ Advanced Filters")
    col1, col2 = st.columns(2)

    with col1:
        # Theme filter with all available themes
        available_themes = [
            '💕 Romance', '✨ Fluff', '🔥 Explicit', '😢 Angst',
            '😱 Horror/Fear', '⚔️ Action', '😂 Humor', '🎭 Drama',
            '🔮 Fantasy', '🚀 Sci-Fi', '🌸 Slice of Life', '🎨 Creative Writing'
        ]
        selected_themes = st.multiselect(
            "🎨 Filter by themes",
            options=available_themes,
            help="Shows conversations containing these themes"
        )

    with col2:
        character_search = st.text_input(
            "👤 Search for characters",
            placeholder="e.g., Harry, Hermione, Ron",
            help="Find conversations mentioning these character names (comma-separated)"
        )

    # Sort options
    sort_option = st.selectbox(
        "✨ Sort by",
        ["Recent first", "Oldest first", "Title A-Z", "Most messages"]
    )

    st.markdown("<div class='lace-divider'></div>", unsafe_allow_html=True)

    # Apply filters
    filtered_convos = conversations

    # Check if filtering by character from gallery
    if 'filter_character' in st.session_state and st.session_state.filter_character:
        gallery_char = st.session_state.filter_character
        st.info(f"🦇 Showing threads featuring **{gallery_char}** (click button again to clear)")

        # Clear button
        if st.button("✨ Clear character filter"):
            st.session_state.filter_character = None
            st.rerun()

        # Apply gallery character filter
        filtered_convos = filter_by_characters(filtered_convos, [gallery_char])

    # Text search (in titles and/or content)
    if search_query:
        filtered_convos = search_conversations(
            filtered_convos,
            search_query,
            search_content=search_in_content,
            search_titles=True
        )

    # Theme filter
    if selected_themes:
        filtered_convos = filter_by_themes(filtered_convos, selected_themes)

    # Character filter from text input
    if character_search:
        character_names = [name.strip() for name in character_search.split(',') if name.strip()]
        if character_names:
            filtered_convos = filter_by_characters(filtered_convos, character_names)

    # Sort conversations
    if sort_option == "Recent first":
        filtered_convos.sort(key=lambda x: x.get('create_time', 0), reverse=True)
    elif sort_option == "Oldest first":
        filtered_convos.sort(key=lambda x: x.get('create_time', 0))
    elif sort_option == "Title A-Z":
        filtered_convos.sort(key=lambda x: x.get('title', '').lower())
    elif sort_option == "Most messages":
        filtered_convos.sort(key=lambda x: len(x.get('messages', [])), reverse=True)

    st.markdown(f"**{len(filtered_convos)}** conversations found 💜")
    st.markdown("<div class='lace-divider'></div>", unsafe_allow_html=True)

    # Display conversations
    for idx, convo in enumerate(filtered_convos):
        title = convo.get('title', 'Untitled Conversation')
        create_time = datetime.fromtimestamp(convo.get('create_time', 0))
        message_count = len(convo.get('messages', []))

        # Detect themes and characters for this conversation
        themes = detect_themes(convo)
        characters = detect_characters(convo, min_mentions=3)

        with st.expander(f"💬 {title}"):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**Created:** {create_time.strftime('%B %d, %Y at %I:%M %p')}")
            with col2:
                st.markdown(f"**Messages:** {message_count}")
            with col3:
                if st.button("👁️ View", key=f"view_{idx}"):
                    st.session_state[f'viewing_{idx}'] = True

            # Show detected themes and characters
            if themes or characters:
                st.markdown("---")

                if themes:
                    st.markdown("**🎨 Detected Themes:**")
                    theme_badges = " ".join([f"`{theme}`" for theme in themes])
                    st.markdown(theme_badges)

                if characters:
                    st.markdown("**👤 Main Characters:**")
                    char_list = ", ".join([f"**{c['name']}** ({c['mentions']}×)" for c in characters[:5]])  # Top 5
                    st.markdown(char_list)

            # Show conversation if viewing
            if st.session_state.get(f'viewing_{idx}', False):
                st.markdown("---")
                show_conversation_thread(convo)

                # Export buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📄 Export to Word", key=f"word_{idx}"):
                        doc_bytes = export_to_word(convo)
                        st.download_button(
                            "💜 Download Word Doc",
                            doc_bytes,
                            file_name=f"{title}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_word_{idx}"
                        )

                with col2:
                    if st.button("📑 Export to PDF", key=f"pdf_{idx}"):
                        pdf_bytes = export_to_pdf(convo)
                        st.download_button(
                            "💜 Download PDF",
                            pdf_bytes,
                            file_name=f"{title}.pdf",
                            mime="application/pdf",
                            key=f"dl_pdf_{idx}"
                        )

def show_conversation_thread(convo):
    """Display full conversation thread with pretty formatting! 💜"""

    messages = convo.get('messages', [])

    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        timestamp = datetime.fromtimestamp(msg.get('create_time', 0))

        # Color-coded by role
        if role == 'user':
            color = "#b4d4f0"  # Pastel blue
            emoji = "👤"
        elif role == 'assistant':
            color = "#c9f0b4"  # Pastel green
            emoji = "🤖"
        else:
            color = "#e8b4f0"  # Pastel purple
            emoji = "💬"

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2d1b3d 0%, #3d2548 100%);
                    border-left: 4px solid {color};
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(232, 180, 240, 0.1);'>
            <div style='color: {color}; font-weight: bold; margin-bottom: 5px;'>
                {emoji} {role.upper()}
                <span style='font-size: 12px; opacity: 0.7; float: right;'>
                    {timestamp.strftime('%I:%M %p')}
                </span>
            </div>
            <div style='color: #e8b4f0; white-space: pre-wrap;'>{content}</div>
        </div>
        """, unsafe_allow_html=True)

def show_about_page():
    """About page with info! 💜"""

    st.markdown("## 📊 About This App")

    st.markdown("""
    ### 🌙✨ Welcome to the Pastel Goth ChatGPT Parser! ✨🌙

    This adorable little app helps you:

    - 💜 **Upload** your ChatGPT export files (ZIP or JSON)
    - 🔍 **Search** through all your conversations
    - 👁️ **View** full conversation threads with pretty formatting
    - 📄 **Export** to Word documents (.docx)
    - 📑 **Export** to PDF files

    ### ✨ Features ✨

    - **Pastel Goth Aesthetic**: Purple, pink, and black with lace-like decorations 💜🖤
    - **Easy Upload**: Drag and drop your ChatGPT export
    - **Smart Search**: Find conversations by title
    - **Multiple Sort Options**: Recent, oldest, alphabetical, or by message count
    - **Beautiful Formatting**: Color-coded messages and timestamps
    - **Export Options**: Save conversations as Word or PDF

    ### 🦇 Made with love and dark magic 🦇

    Built with Streamlit, styled with pastel goth vibes! 💜✨
    """)

if __name__ == "__main__":
    main()
