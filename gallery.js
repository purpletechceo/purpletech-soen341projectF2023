// JavaScript for the image gallery

// Get references to HTML elements
const gallery = document.querySelector(".gallery");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// Get all the images in the gallery
const images = gallery.getElementsByTagName("img");
let currentIndex = 0; // Current image index

// Function to display the current image
function showImage(index) {
    // Hide all images
    for (let i = 0; i < images.length; i++) {
        images[i].style.display = "none";
    }
    // Display the image at the given index
    images[index].style.display = "block";
}

// Initial display
showImage(currentIndex);

// Event listener for the "Previous" button
prevBtn.addEventListener("click", () => {
    currentIndex--;
    if (currentIndex < 0) {
        currentIndex = images.length - 1; // Loop back to the last image
    }
    showImage(currentIndex);
});

// Event listener for the "Next" button
nextBtn.addEventListener("click", () => {
    currentIndex++;
    if (currentIndex >= images.length) {
        currentIndex = 0; // Loop back to the first image
    }
    showImage(currentIndex);
});
