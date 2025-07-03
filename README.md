# 🎥 Python Media Automation Toolkit

A step-by-step practice repository for automating media tasks with Python — from simple file organizing to AI-powered caption generation and dashboards.

---

## 📌 Overview

This toolkit helps you build your Python skills through **8 focused mini-projects** + **1 integrated final project**.  
Each module builds real-world skills you can use for content creation, editing, social media, or your portfolio.

---

## ✅ Project Roadmap

---

### 1️⃣ **Media File Organizer**

**🎯 Goal**  
Automatically sort your media (images, video, audio) into folders by type or date.

**🧩 Tasks**
- Setup working folder
- Write script using `os` & `shutil`
- Move files by extension
- (Optional) Organize by date using metadata

**⚙️ Skills Learned**  
File handling, modules, string/file manipulation

**✅ Checklist**
- [ ] Read files from folder
- [ ] Parse extensions
- [ ] Create destination folders
- [ ] Move files

---

### 2️⃣ **Caption Generator (Manual)**

**🎯 Goal**  
Generate 3–5 caption templates based on user input or theme.

**🧩 Tasks**
- Prompt for topic
- Use string formatting + `random` library
- Output 3 caption variations

**⚙️ Skills Learned**  
Input/output, randomization, string templates

**✅ Checklist**
- [ ] Accept input
- [ ] Create templates
- [ ] Randomly choose format
- [ ] Print captions

---

### 3️⃣ **Image Editor Tool**

**🎯 Goal**  
Batch edit images: resize to 1080×1080, convert format, add watermark.

**🧩 Tasks**
- Install Pillow
- Load images in folder
- Resize, annotate, save output
- Test with sample images

**⚙️ Skills Learned**  
Image editing, file I/O, loops

**✅ Checklist**
- [ ] Load folder of images
- [ ] Resize to fixed dims
- [ ] Overlay watermark/text
- [ ] Save as JPEG/PNG

---

### 4️⃣ **Video Trimmer**

**🎯 Goal**  
Split long videos into 15-second clips for social media.

**🧩 Tasks**
- Install MoviePy
- Load video
- Slice into chunks
- Export clips

**⚙️ Skills Learned**  
Video handling, time intervals, MoviePy basics

**✅ Checklist**
- [ ] Load MP4 file
- [ ] Define slice duration
- [ ] Loop and export clips
- [ ] Verify outputs

---

### 5️⃣ **Content Performance Dashboard**

**🎯 Goal**  
Visualize performance metrics like likes/comments/shares.

**🧩 Tasks**
- Use sample CSV with engagement data
- Read CSV with Pandas
- Plot top posts, average metrics

**⚙️ Skills Learned**  
Dataframes, matplotlib/seaborn, data visualization

**✅ Checklist**
- [ ] Load dataset
- [ ] Clean/filter data
- [ ] Create plots
- [ ] Annotate insights

---

### 6️⃣ **Auto Quote Poster**

**🎯 Goal**  
Generate stylistic quote images automatically.

**🧩 Tasks**
- Load quotes from text file
- Choose background & fonts
- Center quote on image with Pillow
- Save final graphic

**⚙️ Skills Learned**  
Typography, image composition, batch processing

**✅ Checklist**
- [ ] Read quotes file
- [ ] Setup image canvas
- [ ] Center text
- [ ] Export PNG

---

### 7️⃣ **Trend Tracker**

**🎯 Goal**  
Fetch trending YouTube video titles or Google Trends keywords.

**🧩 Tasks**
- Identify target site
- Scrape with BeautifulSoup
- Extract and save top trends

**⚙️ Skills Learned**  
Requests, HTML parsing, automation

**✅ Checklist**
- [ ] Fetch page content
- [ ] Parse HTML
- [ ] Extract trend list
- [ ] Save as CSV

---

### 8️⃣ **Smart Caption Generator (AI)**

**🎯 Goal**  
Use AI to generate creative captions from a keyword or image.

**🧩 Tasks**
- Integrate OpenAI API (or similar)
- Send prompt & receive caption
- (Optional) Add sentiment label

**⚙️ Skills Learned**  
API integration, prompt design, text handling

**✅ Checklist**
- [ ] Setup API access
- [ ] Define prompt based on input
- [ ] Parse response
- [ ] Display caption

---

## 🎯 Final Project – Social Media Toolkit

**🎯 Goal**  
An integrated tool to create, caption, and track content.

**🧩 Tasks**
- Combine image editing + AI caption
- Add module to read recent post metrics
- Build simple UI (Tkinter or Streamlit)

**⚙️ Skills Learned**  
Modular architecture, combining tools, UI basics

**✅ Checklist**
- [ ] Set up input for image
- [ ] Call image editor & caption generator
- [ ] Load CSV of previous metrics
- [ ] Display a summary & new caption

---

## 📚 How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Automated_python_media_toolkit.git
   cd Automated_python_media_toolkit
