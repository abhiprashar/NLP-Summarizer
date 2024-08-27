// Function to handle file upload
document.getElementById("upload-file").addEventListener("change", function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const text = event.target.result;
            document.getElementById("input-text").value = text;
        };
        reader.readAsText(file);
    }
});

// Function to style the upload button on hover
const uploadButton = document.getElementById("upload-button");
uploadButton.addEventListener("mouseover", function() {
    this.style.backgroundColor = "#333";
    this.style.color = "#fff";
});

uploadButton.addEventListener("mouseout", function() {
    this.style.backgroundColor = "beige";
    this.style.color = "#333";
});
