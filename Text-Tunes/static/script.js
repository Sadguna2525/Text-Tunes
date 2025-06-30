const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const chooseFileButton = document.getElementById('choose-file-button');
const submitButton = document.getElementById('submit-button');
const fileNameDisplay = document.getElementById('file-name-display');
const audioControls = document.getElementById('audio-controls');
const audioPlayer = document.getElementById('audio-player');
const downloadLink = document.getElementById('download-link');

// Function to handle file selection and display file name
function handleFileSelection(file) {
    if (file) {
        if (file.type === 'application/pdf') {
            fileNameDisplay.textContent = `Selected file: ${file.name}`;
            return true;
        } else {
            fileNameDisplay.textContent = 'Only PDF files are allowed!';
            alert('Only PDF files are allowed!');
            return false;
        }
    }
    else {
        fileNameDisplay.textContent = 'No file selected';
    }
}

// Event listeners
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files; // Populate file input
    handleFileSelection(file);
});

dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFileSelection(file);
});

chooseFileButton.addEventListener('click', () => {
    fileInput.click();
});

submitButton.addEventListener('click', () => {
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    audioPlayer.src = data.audio_url;
                    downloadLink.href = data.audio_url;
                    audioControls.style.display = 'block';
                    audioPlayer.load(); // Ensure the audio is loaded
                    audioPlayer.play(); // Play the audio automatically
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert('No file selected!');
    }
});






