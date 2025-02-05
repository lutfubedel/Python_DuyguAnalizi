function analyzeSentiment() {
    const sentence = document.getElementById("sentence").value;
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    if (sentence.trim() === "") {
        alert("Lütfen bir cümle girin!");
        return;
    }

    loading.style.display = "block";
    result.textContent = "";

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: sentence })
    })
    .then(response => response.json())
    .then(data => {

        loading.style.display = "none";

        if (data.error) {
            result.textContent = "Hata: " + data.error;
        } else {
            let sentiment = data.sentiment;
            result.textContent = "Duygu Analizi Sonucu: " + (typeof sentiment === "number" ? sentiment.toFixed(2) : sentiment);
        }
    })
    .catch(error => {
        console.error("Hata:", error);
        result.textContent = "Sunucuya bağlanırken hata oluştu.";
        loading.style.display = "none";
    });
}
