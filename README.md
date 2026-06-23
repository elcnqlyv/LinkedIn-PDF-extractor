# LinkedIn Document to PDF Scraper

A simple, two-step tool to extract and compile non-downloadable PDF documents from LinkedIn profiles. Since LinkedIn's document viewer only allows viewing page-by-page and blocks direct downloads, this tool extracts the cached image URLs from your browser and stitches them back together into a single, clean PDF file.

## ⚙️ Requirements

Before you begin, ensure you have the following installed on your system:
- **Python 3.x** installed and added to your system PATH.
- **A modern web browser** (Chrome, Firefox, Edge, etc.).
- **Python Libraries:** `requests` and `img2pdf`.

### Install Python Dependencies
Open your terminal or command prompt and run:
```bash
pip install requests img2pdf
```

---

## 🛠️ How It Works

The process is divided into two phases:
1. **Browser Extraction:** You scroll through the document on LinkedIn to load the pages into your browser's cache. A JavaScript snippet then extracts the direct image URLs for each page and saves them to a text file.
2. **Python Compilation:** A Python script reads that text file, downloads the individual page images, and losslessly compiles them into a single PDF document.

---

## 🚀 Step-by-Step Usage Guide

### Step 1: Load the Document in LinkedIn
1. Go to the LinkedIn profile containing the project document you want to download.
2. Open the document viewer.
3. **Crucial:** Scroll slowly from the first page to the very last page. This ensures every page is fully loaded into your browser's cache.

### Step 2: Extract the URLs via Browser Console
1. While the document viewer is open, press `F12` (or right-click and select **Inspect**) to open the Developer Tools.
2. Navigate to the **Console** tab.
3. Paste the following JavaScript code and press **Enter**:

```javascript
(() => {
  const pageImages = Array.from(document.querySelectorAll('img'))
    .map(img => img.src)
    .filter(src => src.includes('profile-treasury-document-images'));

  const uniqueUrls = [...new Set(pageImages)];

  if (uniqueUrls.length === 0) {
    console.error("No pages found. Make sure the document viewer is completely open and scrolled through!");
    return;
  }

  const textContent = uniqueUrls.join('\n');
  const blob = new Blob([textContent], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'linkedin_doc_urls.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  console.log(`Success! Created a file with all ${uniqueUrls.length} full, un-truncated URLs.`);
})();
```

4. This will automatically download a file named `linkedin_doc_urls.txt` to your default downloads folder.

### Step 3: Compile the PDF
1. Move the downloaded `linkedin_doc_urls.txt` into the same directory as your `compile_linkedin_pdf.py` script.
2. Open your terminal/command prompt in that directory.
3. Run the Python script:
```bash
python compile_linkedin_pdf.py
```
4. The script will download each page image, compile them into `LinkedIn_Treasury_Document.pdf`, and automatically clean up all temporary files (including the URL list).

---

## 🧹 Manual Cleanup & Troubleshooting

If you ever need to manually clean up leftover files from a failed run or a previous test, you can use these commands:

**Windows:**
```cmd
del linkedin_doc_urls.txt LinkedIn_Treasury_Document.pdf
rmdir /s /q downloaded_pages
```

**Mac/Linux:**
```bash
rm -f linkedin_doc_urls.txt LinkedIn_Treasury_Document.pdf
rm -rf downloaded_pages
```

### Troubleshooting
- **"No pages found" error:** Ensure you scrolled through the *entire* document in the browser before running the JavaScript snippet. The images only load into the DOM/cache when they are scrolled into view.
- **Missing Pages:** If the script reports missing pages, simply re-run `python compile_linkedin_pdf.py`. It has resume support and will only download the pages that failed or are missing.

---

## ⚠️ Disclaimer
This tool is intended for educational purposes and personal archiving of documents you have legitimate access to view. Please respect LinkedIn's Terms of Service and the intellectual property rights of the content creators.
