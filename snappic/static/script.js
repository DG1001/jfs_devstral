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
    } catch (error) {
        console.error(error);
        alert('Error uploading file');
    }
});
