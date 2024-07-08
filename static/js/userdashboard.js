document.addEventListener("DOMContentLoaded", (event) => {
    const modal = document.getElementById("fileModal");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const modalDownload = document.getElementById("modal-download");
    const modalEmail = document.getElementById("modal-email");
    const span = document.getElementsByClassName("close")[0];

    // Open button click event
    document.querySelectorAll(".open-btn").forEach((button) => {
      button.addEventListener("click", function () {
        const title = this.getAttribute("data-title");
        const description = this.getAttribute("data-description");
        const fileUrl = this.getAttribute("data-file-url");
        const documentId = this.getAttribute("data-document-id");

        modalTitle.textContent = title;
        modalDescription.textContent = description;
        modalDownload.href = `/download-file/${documentId}/`;
        modalEmail.href = `/email/${documentId}/`;

        modal.style.display = "block";
      });
    });

    // Close button event
    span.onclick = function () {
      modal.style.display = "none";
    };

    // Click outside of modal to close it
    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };

    // Email button click event
    document.querySelectorAll(".email-btn").forEach((button) => {
      button.addEventListener("click", function () {
        const documentId = this.getAttribute("data-document-id");
        window.location.href = `/email/${documentId}/`;
      });
    });

    // Multiple download button click event
    const downloadButton = document.getElementById("download-selected");
    downloadButton.addEventListener("click", function () {
      const selectedFiles = document.querySelectorAll(
        ".select-file:checked"
      );
      const fileIds = Array.from(selectedFiles).map((cb) =>
        cb.getAttribute("data-file-id")
      );

      if (fileIds.length > 0) {
        const formData = new FormData();
        formData.append("file_ids", JSON.stringify(fileIds));

        fetch("/download-multiple/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => response.blob())
          .then((blob) => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "files.zip";
            document.body.appendChild(a);
            a.click();
            a.remove();
          })
          .catch((error) => console.error("Error:", error));
      } else {
        alert("Please select at least one file to download.");
      }
    });

    // Function to retrieve CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; cookies.length > i; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(
              cookie.substring(name.length + 1)
            );
            break;
          }
        }
      }
      return cookieValue;
    }
  });