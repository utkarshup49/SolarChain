//window.addEventListener('scroll', function() {
//    const video = document.querySelector('video');
//    const scrollPosition = window.scrollY;
//    const blurValue = Math.min(scrollPosition / 100, 8); // Adjust the denominator for sensitivity (100 in this case)
//
//    // Apply the blur based on the scroll position
//    video.style.filter = `blur(${blurValue}px)`;
//    video.style.webkitFilter = `blur(${blurValue}px)`; // For Safari support
//
//    const alphaValue = Math.max(Math.min(scrollPosition / 500, 0.6), 0.4);
//    document.querySelector('.video-bg').style.setProperty('--bg-alpha', alphaValue);
//});
