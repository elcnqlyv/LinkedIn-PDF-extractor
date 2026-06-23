import os
import re
import requests
import img2pdf

# Configuration
URL_FILE = "linkedin_doc_urls.txt"
OUTPUT_PDF = "LinkedIn_Treasury_Document.pdf"
CACHE_DIR = "downloaded_pages"

# Setup headers to look like a standard web browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def extract_urls(file_path):
    """Reads the text file and cleans up lines to extract pure URLs."""
    urls = []
    if not os.path.exists(file_path):
        print(f"[-] Error: Could not find '{file_path}' in this directory.")
        return urls

    with open(file_path, "r") as f:
        for line in f:
            # Use regex to find the actual URL, stripping out bits like ''
            match = re.search(r"https://media\.licdn\.com/[^\s\"]+", line)
            if match:
                urls.append(match.group(0))
    return urls


def download_pages(urls, cache_dir):
    """Downloads images sequentially with resume support to handle network drops."""
    os.makedirs(cache_dir, exist_ok=True)
    downloaded_files = []
    total_pages = len(urls)

    print(
        f"[+] Found {total_pages} pages in your URL list. Starting download pipeline..."
    )

    for index, url in enumerate(urls, start=1):
        # Format filename symmetrically (e.g., page_001.jpg) to preserve correct sorting order
        filename = os.path.join(cache_dir, f"page_{index:03d}.jpg")
        downloaded_files.append(filename)

        # Check if page was already fetched in a previous attempt
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            if response.status_code == 200:
                with open(filename, "wb") as img_file:
                    img_file.write(response.content)
                if index % 10 == 0 or index == total_pages:
                    print(f"[✓] Progress: {index}/{total_pages} pages downloaded.")
            else:
                print(
                    f"[X] Failed to download page {index} (HTTP Status: {response.status_code})"
                )
        except Exception as e:
            print(f"[X] Network interruption on page {index}: {e}")
            print("[-] Run the script again to resume from this page.")
            return []

    return downloaded_files


def compile_to_pdf(image_paths, output_path):
    """Losslessly wraps the sequential images into a single PDF document."""
    print(f"\n[+] All pages collected. Compiling into '{output_path}'...")
    try:
        # Sort files explicitly to guarantee pages are arranged chronologically
        image_paths.sort()

        with open(output_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(image_paths))

        print(
            f"[✓] Success! Final compiled document ready at: {os.path.abspath(output_path)}"
        )

        # Optional cleanup of individual image cache files
        print("[+] Cleaning up temporary image directory...")
        for path in image_paths:
            os.remove(path)
        os.rmdir(os.path.dirname(image_paths[0]))
        print("[✓] Temporary files cleared.")

    except Exception as e:
        print(f"[-] Compilation failed: {e}")


if __name__ == "__main__":
    # 1. Parse and sanitize links
    target_urls = extract_urls(URL_FILE)

    if target_urls:
        # 2. Safely scrape individual files to storage
        image_list = download_pages(target_urls, CACHE_DIR)

        # 3. Build the PDF if all files fetched successfully
        if len(image_list) == len(target_urls):
            compile_to_pdf(image_list, OUTPUT_PDF)
        else:
            print(
                "[-] Process incomplete. Please re-run the script to catch missing frames."
            )
