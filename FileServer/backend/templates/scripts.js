document.addEventListener('DOMContentLoaded', () => {
    const fileModal = document.getElementById('fileModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalDownloadLink = document.getElementById('modalDownloadLink');
    const closeModalButton = document.querySelector('.modal .close');

    // Add event listener to open buttons
    document.querySelectorAll('.open-btn').forEach(button => {
        button.addEventListener('click', () => {
            const title = button.getAttribute('data-title');
            const description = button.getAttribute('data-description');
            const fileUrl = button.getAttribute('data-file-url');

            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalDownloadLink.setAttribute('href', fileUrl);

            fileModal.style.display = 'block';
        });
    });

    // Close the modal
    closeModalButton.addEventListener('click', () => {
        fileModal.style.display = 'none';
    });

    // Close modal when clicking outside of the modal content
    window.addEventListener('click', (event) => {
        if (event.target === fileModal) {
            fileModal.style.display = 'none';
        }
    });
});
