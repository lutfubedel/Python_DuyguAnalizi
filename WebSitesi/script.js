document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("text-input");
    const analyzeButton = document.getElementById("analyze-btn");
    const resultContainer = document.getElementById("result-container");
    const loadingSpinner = document.getElementById("loading-spinner");

    analyzeButton.addEventListener("click", function () {
        analyzeSentiment(inputField.value);
    });

    inputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            analyzeSentiment(inputField.value);
        }
    });

    // Listen for input changes to hide result when empty
    inputField.addEventListener("input", function () {
        if (!inputField.value.trim()) {
            resultContainer.style.display = "none";
        }
    });

    function analyzeSentiment(text) {
        if (!text.trim()) {
            resultContainer.textContent = "Lütfen bir cümle girin!";
            resultContainer.style.backgroundColor = "#ffcccc"; // Light red for warning
            resultContainer.style.display = "block";
            return;
        }

        // Show the spinner and clear previous result
        resultContainer.style.display = "none";
        loadingSpinner.style.display = "block";

        fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.json())
        .then(data => {
            // Hide spinner
            loadingSpinner.style.display = "none";

            if (data.error) {
                resultContainer.textContent = data.error;
                resultContainer.style.backgroundColor = "#ffcccc"; // Light red
            } else {
                resultContainer.textContent = `Sonuç: ${data.sentiment}`;
                resultContainer.style.backgroundColor = data.sentiment === "Pozitif" ? "#b8e6b8" : "#f5b7b1"; // Green for positive, red for negative
            }
            resultContainer.style.display = "block"; // Show result
        })
        .catch(error => {
            console.error("Hata:", error);
            resultContainer.textContent = "Sunucu hatası!";
            resultContainer.style.backgroundColor = "#ff5757";
            resultContainer.style.display = "block";
            loadingSpinner.style.display = "none"; // Hide spinner if an error occurs
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const themeButton = document.getElementById("theme-btn");
    const themeIcon = document.getElementById("theme-icon");

    function updateThemeIcon() {
        const isDarkMode = document.body.classList.contains("dark-mode");
        themeIcon.src = isDarkMode
            ? "https://cdn-icons-png.flaticon.com/512/581/581601.png" // Crescent Moon for Dark Mode
            : "https://cdn-icons-png.flaticon.com/512/439/439842.png"; // Sun for Light Mode
    }

    themeButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        updateThemeIcon();
    });

    updateThemeIcon();
});

document.addEventListener("DOMContentLoaded", function () {
    const contactBtn = document.getElementById("contact-btn");
    const popupOverlay = document.getElementById("popup-overlay");
    const closePopup = document.getElementById("close-popup");

    // Ensure popup is hidden when page loads
    popupOverlay.style.display = "none";

    // Open popup when clicking the contact button
    contactBtn.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent link default action
        popupOverlay.style.display = "flex";
    });

    // Close popup when clicking the close button
    closePopup.addEventListener("click", function () {
        popupOverlay.style.display = "none";
    });

    // Close popup when clicking outside the popup content
    popupOverlay.addEventListener("click", function (event) {
        if (event.target === popupOverlay) {
            popupOverlay.style.display = "none";
        }
    });
});


