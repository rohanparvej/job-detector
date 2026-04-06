document.addEventListener("DOMContentLoaded", () => {
    const detectBtn = document.querySelector(".detect-btn");
    const jobTextInput = document.getElementById("jobText");
    
    // Result elements
    const predictionEl = document.getElementById("prediction");
    const realProbEl = document.getElementById("realProb");
    const fakeProbEl = document.getElementById("fakeProb");
    const riskEl = document.getElementById("risk");
    // Add this at the top of your script
    fetch("https://job-detector.onrender.com/")
    .then(res => res.json())
    .then(data => console.log("Backend Status:", data.status))
    .catch(err => console.error("Backend is offline"));
    detectBtn.addEventListener("click", async () => {
        const text = jobTextInput.value.trim();

        if (!text) {
            alert("Please paste a job description first!");
            return;
        }

        // Show a loading state
        detectBtn.textContent = "Analyzing...";
        detectBtn.disabled = true;

        try {
            const response = await fetch("https://job-detector.onrender.com/predict", {
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
                throw new Error("Server error. Make sure FastAPI is running.");
            }

            const data = await response.json();

            // Update the UI with the response from FastAPI
            predictionEl.textContent = data.label;
            
            // Calculate probabilities for the display
            // (Assuming data.probability is the 'Fake' probability)
            const fakeVal = data.probability;
            const realVal = (100 - fakeVal).toFixed(2);

            realProbEl.textContent = `${realVal}%`;
            fakeProbEl.textContent = `${fakeVal}%`;
            riskEl.textContent = data.risk;

            // Optional: Change color based on prediction
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
