document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const textSizeDisplay = document.getElementById('text-size-display');
    const imageSizeDisplay = document.getElementById('image-size-display');
    const images = document.querySelectorAll('.sample-image');
    const popup = document.getElementById('filter-popup');

    // Access Flask variables from window.flaskData
    let currentTextSize = window.flaskData.textSize;
    let currentImageSize = window.flaskData.imageSize;

    body.style.fontSize = currentTextSize + 'px';
    images.forEach(img => img.style.width = currentImageSize + 'px');

    textSizeDisplay.textContent = `Your predicted text size: ${currentTextSize}px`;
    imageSizeDisplay.textContent = `Your predicted image size: ${currentImageSize}px`;

    function adjustTextSize(change) {
        let newSize = currentTextSize + change;
        newSize = Math.max(10, Math.min(45, newSize));
        currentTextSize = newSize;
        body.style.fontSize = newSize + 'px';
        textSizeDisplay.textContent = `Your predicted text size: ${newSize}px`;
    }

    function adjustImageSize(change) {
        let newSize = currentImageSize + change;
        newSize = Math.max(50, Math.min(500, newSize));
        currentImageSize = newSize;
        images.forEach(img => img.style.width = newSize + 'px');
        imageSizeDisplay.textContent = `Your predicted image size: ${newSize}px`;
    }

    function showPopup() {
        popup.classList.add('show');
    }

    function closePopup() {
        popup.classList.remove('show');
    }

    // Show popup on page load
    showPopup();

    document.getElementById('text-increase').addEventListener('click', () => adjustTextSize(2));
    document.getElementById('text-decrease').addEventListener('click', () => adjustTextSize(-2));
    document.getElementById('image-increase').addEventListener('click', () => adjustImageSize(10));
    document.getElementById('image-decrease').addEventListener('click', () => adjustImageSize(-10));
    document.getElementById('accept-settings').addEventListener('click', closePopup);
});