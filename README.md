# 🌙✨ Pastel Goth ChatGPT Export Parser ✨🌙

A beautifully designed Streamlit app for viewing and exporting your ChatGPT conversations with **adorable pastel goth aesthetics**! 💜🖤

![Pastel Goth Vibes](https://img.shields.io/badge/aesthetic-pastel_goth-b794c9?style=for-the-badge)
![Made with Love](https://img.shields.io/badge/made_with-love_and_dark_magic-e8b4f0?style=for-the-badge)

## ✨ Features

- 💜 **Beautiful Pastel Goth UI** - Purple, pink, and black color scheme with lace-like decorative elements
- 📦 **Easy Upload** - Support for both ZIP and JSON ChatGPT exports
- 🔍 **Advanced Search** - Search in both titles AND message content!
- 🎨 **Theme Detection** - Automatically detects content themes like Romance, Fluff, Explicit, Angst, Horror, Action, Humor, and more!
- 👤 **Character Detection** - Smart AI finds recurring character names mentioned in conversations
- 🎭 **Rogue's Gallery** - Sidebar character analytics! See all your RP partners with thread counts, total mentions, and dominant themes
- 🦇 **One-Click Character Filter** - Click any character in the gallery to instantly filter to their threads
- 🎭 **Content Filtering** - Filter conversations by detected themes or character names
- 📊 **Multiple Sort Options** - Sort by date, title, or message count
- 💬 **Beautiful Conversation Viewer** - Color-coded messages with timestamps
- 📄 **Word Export** - Download conversations as .docx files with pastel styling
- 📑 **PDF Export** - Generate beautiful PDF documents
- 🌙 **Adorable Design** - Every detail crafted with love and dark magic!

## 🚀 Quick Start

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd gpt_pdf
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501` 💜

## 📖 How to Use

### Getting Your ChatGPT Export

1. Go to [ChatGPT](https://chat.openai.com)
2. Click on your profile → **Settings** ⚙️
3. Navigate to **Data controls**
4. Click **Export data**
5. Wait for the email (usually takes a few minutes to a day)
6. Download the ZIP file from the email

### Using the App

1. **Upload** - Drop your ChatGPT export (ZIP or JSON) in the upload area
2. **Browse** - See all your conversations with titles, dates, and message counts
3. **Advanced Search** 🔍:
   - **Text Search**: Search in titles and/or message content
   - **Theme Filter**: Select themes like Romance 💕, Fluff ✨, Angst 😢, Horror 😱, and more
   - **Character Search**: Enter character names (comma-separated) to find conversations mentioning them
   - Themes and characters are automatically detected for each conversation!
4. **Sort** - Choose how to organize your conversations (Recent, Oldest, A-Z, Most messages)
5. **View Details** - Each conversation shows:
   - Detected themes with cute emoji tags
   - Main characters with mention counts
   - Full message thread when you click "View"
6. **Export** - Download individual conversations as Word or PDF files

## 🎨 Aesthetic Details

This app features a carefully crafted **pastel goth** aesthetic:

- **Colors**: Soft purples (#e8b4f0, #c9a3d8, #b794c9) mixed with dark backgrounds
- **Fonts**: Elegant Georgia serif font
- **Effects**: Lace-like dividers, gradient backgrounds, glowing shadows
- **Emojis**: Moons, stars, hearts, and gothic decorations throughout
- **Animations**: Smooth hover effects and sparkle animations

## 🛠️ Technical Stack

- **Streamlit** - Web framework
- **Python 3.7+** - Core language
- **python-docx** - Word document generation
- **reportlab** - PDF generation

## 📦 Project Structure

```
gpt_pdf/
├── app.py                 # Main Streamlit app with UI
├── chatgpt_export.py      # ChatGPT parser and export logic
├── requirements.txt       # Python dependencies
└── README.md             # This file!
```

## 💜 Features in Detail

### Parser
- Handles ChatGPT's tree-based conversation structure
- Extracts linear message threads
- Preserves timestamps and metadata
- Supports both ZIP and JSON formats

### Advanced Search & Filter 🔍✨

**Text Search:**
- Search in conversation titles
- Search within message content
- Toggle between title-only or full content search
- Case-insensitive matching

**Theme Detection:**
Automatically detects 12 different content themes:
- 💕 **Romance** - Love, dating, relationships
- ✨ **Fluff** - Cute, wholesome, cozy content
- 🔥 **Explicit** - Mature/NSFW content
- 😢 **Angst** - Sad, emotional, heartbreaking
- 😱 **Horror/Fear** - Scary, creepy, dark themes
- ⚔️ **Action** - Fighting, battles, combat
- 😂 **Humor** - Funny, comedy, jokes
- 🎭 **Drama** - Conflict, tension, emotional intensity
- 🔮 **Fantasy** - Magic, dragons, mythical creatures
- 🚀 **Sci-Fi** - Space, technology, futuristic
- 🌸 **Slice of Life** - Everyday, realistic scenarios
- 🎨 **Creative Writing** - Stories, fanfiction, roleplay

**Character Detection:**
- Smart pattern matching finds capitalized names
- Filters out common words
- Counts mentions to identify main characters
- Shows top 5 characters per conversation
- Search for specific characters across all conversations

**🎭 Rogue's Gallery (Sidebar Analytics):**
Perfect for roleplay tracking! The sidebar displays:
- **Character Profiles**: All detected characters sorted by thread count
- **Thread Count**: How many conversations each character appears in
- **Total Mentions**: Sum of all mentions across all threads
- **Dominant Themes**: Top 3 themes associated with each character
- **One-Click Filtering**: Click "Show [Character]'s threads" to instantly filter
- **Clear Overview**: See your RP partners at a glance (Lyra, Lucius Malfoy, Captain Hook, etc!)

### Export Formats

**Word (.docx)**
- Color-coded role labels
- Formatted timestamps
- Proper spacing and indentation
- Pastel purple styling

**PDF**
- Professional layout
- Color-coded messages
- Embedded fonts
- Clean formatting

## 🌙 Coming Soon

Ideas for future updates:
- 📊 Conversation statistics dashboard
- 🎨 Custom theme selector
- 🔍 Advanced search (content search)
- 📥 Batch export all conversations
- 💾 Bookmark favorite conversations

## 🤝 Contributing

Feel free to submit issues or pull requests! Let's make this even more adorable together! 💜✨

## 📝 License

This project is open source and available for personal use. Made with love and dark magic! 🦇

## 💖 Acknowledgments

Built with:
- Love 💜
- Coffee ☕
- Pastel goth vibes 🌙
- A sprinkle of dark magic ✨

---

<p align="center">
Made with 💜 by an adorable little algorithm
</p>

<p align="center">
🦇 Embrace the pastel darkness 🦇
</p>
