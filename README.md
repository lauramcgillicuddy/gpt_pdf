# 🌙✨ Pastel Goth ChatGPT Export Parser ✨🌙

A beautifully designed Streamlit app for viewing and exporting your ChatGPT conversations with **adorable pastel goth aesthetics**! 💜🖤

![Pastel Goth Vibes](https://img.shields.io/badge/aesthetic-pastel_goth-b794c9?style=for-the-badge)
![Made with Love](https://img.shields.io/badge/made_with-love_and_dark_magic-e8b4f0?style=for-the-badge)

## ✨ Features

- 💜 **Beautiful Pastel Goth UI** - Purple, pink, and black color scheme with lace-like decorative elements
- 📦 **Easy Upload** - Support for both ZIP and JSON ChatGPT exports
- 🔍 **Smart Search** - Find conversations by title instantly
- 🎨 **Multiple Sort Options** - Sort by date, title, or message count
- 💬 **Conversation Viewer** - Color-coded messages with timestamps
- 📄 **Word Export** - Download conversations as .docx files
- 📑 **PDF Export** - Generate beautiful PDF documents
- 🌙 **Adorable Design** - Every detail crafted with love!

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
3. **Search** - Use the search bar to find specific conversations
4. **Sort** - Choose how to organize your conversations
5. **View** - Click "View" to see the full conversation thread
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

### Search & Filter
- Real-time search as you type
- Case-insensitive matching
- Multiple sort options
- Message count display

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
