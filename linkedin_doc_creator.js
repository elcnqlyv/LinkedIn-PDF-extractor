(() => {
  const pageImages = Array.from(document.querySelectorAll('img'))
    .map(img => img.src)
    .filter(src => src.includes('profile-treasury-document-images'));

  const uniqueUrls = [...new Set(pageImages)];

  if (uniqueUrls.length === 0) {
    console.error("No pages found. Make sure the document viewer is completely open!");
    return;
  }

  // Create a blob file containing all clean URLs and trigger an automatic download
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
