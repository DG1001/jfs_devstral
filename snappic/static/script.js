document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (event) => {
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
                loadGallery(); // Reload the gallery after a successful upload
            } catch (error) {
                console.error(error);
                alert('Error uploading file');
            }
        });
    }

    async function loadGallery() {
        const response = await fetch('/api/images');
        if (!response.ok) {
            throw new Error('Failed to load images');
        }

        const metadata = await response.json();
        const gallery = document.getElementById('imageGallery');

        // Clear the current gallery
        gallery.innerHTML = '';

        // Add new images to the gallery
        metadata.forEach(image => {
            const imageItem = document.createElement('div');
            imageItem.classList.add('image-item');
            imageItem.dataset.expiration = image.expiration;

            const img = document.createElement('img');
            img.src = `/uploads/${image.filename}`;
            img.alt = image.comment;

            const comment = document.createElement('p');
            comment.textContent = image.comment;

            imageItem.appendChild(img);
            imageItem.appendChild(comment);
            gallery.appendChild(imageItem);

            // Start fade-out timer
            setTimeout(() => {
                imageItem.classList.add('fade-out');
            }, 5000); // Fade out after 5 seconds
        });
    }

    // Load the gallery on page load
    window.onload = loadGallery;
});
