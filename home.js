document.getElementById('menuToggle').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
});
const fileInput = document.getElementById('fileInput');
const submitButton = document.getElementById('submitButton');

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        submitButton.style.display = 'block';
    } else {
        submitButton.style.display = 'none';
    }
});
