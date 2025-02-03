function analyzeSentiment() {
    const sentence = document.getElementById("sentence").value;
    if (sentence.trim() === "") {
        alert("Lütfen bir cümle girin!");
        return;
    }

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: sentence })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").textContent = "Hata: " + data.error;
        } else {
            let sentiment = data.sentiment;
            
            // Eğer sentiment sayısal değilse hata olmasın diye string olarak gösterelim
            if (typeof sentiment === "number") {
                document.getElementById("result").textContent = "Duygu Analizi Sonucu: " + sentiment.toFixed(2);
            } else {
                document.getElementById("result").textContent = "Duygu Analizi Sonucu: " + sentiment;
            }
        }
    })
    .catch(error => {
        console.error("Hata:", error);
        document.getElementById("result").textContent = "Sunucuya bağlanırken hata oluştu.";
    });
}