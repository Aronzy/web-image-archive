// Read-only DOM expression. Evaluate through the current browser's supported API.
// Inspect current page structure first: selectors may change with site updates.
(() => {
  const seen = new Set();
  const images = Array.from(document.querySelectorAll('picture img.img-fit'))
    .filter(image => image.src.includes('/p/assets/images/images/'))
    .filter(image => {
      const key = new URL(image.src).pathname;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .map(image => ({
      url: image.currentSrc || image.src,
      expected_width: image.naturalWidth || null,
      expected_height: image.naturalHeight || null,
      quality: 'best_available',
      quality_evidence: 'Rendered artwork image; uploaded original not confirmed'
    }));
  return {source_page: location.href, title: document.title, images,
    non_image_media: {
      video_count: document.querySelectorAll('video').length,
      embedded_frames: Array.from(document.querySelectorAll('iframe'))
        .filter(frame => /youtube|vimeo|sketchfab/i.test(frame.src))
        .map(frame => ({title: frame.title, source: frame.src.split('?')[0]}))
    }};
})()
