document.addEventListener("DOMContentLoaded", () => {
    const detectBtn = document.querySelector(".detect-btn");
    const jobTextInput = document.getElementById("jobText");
    
    // Result elements
    const predictionEl = document.getElementById("prediction");
    const realProbEl = document.getElementById("realProb");
    const fakeProbEl = document.getElementById("fakeProb");
    const riskEl = document.getElementById("risk");

    // Check backend health using the new /health route
    fetch("/health")
        .then(res => res.json())
        .then(data => console.log("Backend Status:", data.status))
        .catch(err => console.error("Backend is offline"));

    detectBtn.addEventListener("click", async () => {
        const text = jobTextInput.value.trim();

        if (!text) {
            alert("Please paste a job description first!");
            return;
        }

        detectBtn.textContent = "Analyzing...";
        detectBtn.disabled = true;

        try {
            // Use a relative path since frontend and backend are bundled
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: text,
                    extra_features: [
                        document.getElementById("telecommuting").checked ? 1 : 0,
                        document.getElementById("hasLogo").checked ? 1 : 0,
                        document.getElementById("hasQuestions").checked ? 1 : 0
                    ]
                }),
            });

            if (!response.ok) {
                throw new Error("Server error. Make sure your backend is running.");
            }

            const data = await response.json();

            predictionEl.textContent = data.label;
            const fakeVal = data.probability;
            const realVal = (100 - fakeVal).toFixed(2);

            realProbEl.textContent = `${realVal}%`;
            fakeProbEl.textContent = `${fakeVal}%`;
            riskEl.textContent = data.risk;
            predictionEl.style.color = data.prediction === 1 ? "#e74c3c" : "#2ecc71";

        } catch (error) {
            console.error("Error:", error);
            alert("Could not connect to the backend. Check your terminal.");
        } finally {
            detectBtn.textContent = "Detect";
            detectBtn.disabled = false;
        }
    });
});
