// When upload button is clicked, open the file picker dialog.
document.getElementById('uploadButton').addEventListener('click', () => {
    document.getElementById('imageInput').click();
});

// Event listener for when a image is input using 'uploadButton'
document.getElementById('imageInput').addEventListener('change', (event) => {
    const reader = new FileReader();
    reader.onload = () => {
        // Display the selected image on index.html
        document.getElementById('selectedImage').src = reader.result;
        document.getElementById('selectedImage').style.display = 'block';
        // Call the uploadImage function, passing in the first file
        uploadImage(event.target.files[0]);
    };
    // Start reading the selected file as a Data URL
    reader.readAsDataURL(event.target.files[0]);
});


async function uploadImage(file) {
    // Show loading sign while the response is being loaded
    document.getElementById('loading').style.display = 'block';

    // Create a new FormData object to hold the file data
    const formData = new FormData();
    // Append the selected file to the FormData object with the key 'file'
    formData.append('file', file);

    // Send a POST request to the '/predict' endpoint with the form data
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    document.getElementById('artwork').textContent = `Artwork: ${data.artwork}`;
    document.getElementById('artist').textContent = `Artist: ${data.artist}`;
    document.getElementById('prediction').style.display = 'block';
    // Hide the loading sign
    document.getElementById('loading').style.display = 'none';
}
