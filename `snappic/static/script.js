document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        alert('File uploaded successfully');
        event.target.reset();
        loadGallery(); // Reload the gallery after upload
    } catch (error) {
        console.error(error);
        alert('Error uploading file');
    }
});

async function loadGallery() {
    const response = await fetch('/api/images');
    if (!response.ok) {
        throw new Error('Failed to load images');
    }

    const metadata = await response.json();
    const gallery = document.getElementById('gallery');

    // Clear the current gallery
    gallery.innerHTML = '';

    // Add each image to the gallery with expiration timer
    metadata.forEach(entry => {
        const imgContainer = document.createElement('div');
        imgContainer.className = 'image-container';

        const img = document.createElement('img');
        img.src = `/uploads/${entry.filename}`;
        img.alt = entry.comment;

        const comment = document.createElement('p');
        comment.textContent = entry.comment;

        imgContainer.appendChild(img);
        imgContainer.appendChild(comment);

        gallery.appendChild(imgContainer);

        // Set a timer to remove the image after 15 seconds
        setTimeout(() => {
            imgContainer.remove();
        }, 15000); // 15 seconds
    });
}

// Load the gallery on page load
document.addEventListener('DOMContentLoaded', () => {
    loadGallery();
});
