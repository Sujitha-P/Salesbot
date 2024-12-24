const chatBox = document.getElementById('chat-box');
const sentimentChartCtx = document.getElementById('sentiment-chart').getContext('2d');
const intentBox = document.getElementById('intent-box');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
let sentimentChart;
let statusInterval;

// Initialize the chart
function initializeChart() {
    sentimentChart = new Chart(sentimentChartCtx, {
        type: 'pie',
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                data: [0, 0, 0], // Initialize with zero values
                backgroundColor: ['#4caf50', '#f44336', '#9e9e9e'],
            }]
        }
    });
}

// Add a message to the chat box
function addMessage(role, message) {
    const msgDiv = document.createElement('div');
    msgDiv.textContent = `${role === 'user' ? 'You' : 'Bot'}: ${message}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Update the sentiment chart based on sentiment label
function updateChart(sentiment) {
    const sentimentData = {
        Positive: 0,
        Negative: 0,
        Neutral: 0
    };

    if (sentiment === "POSITIVE") {
        sentimentData.Positive = 1;
    } else if (sentiment === "NEGATIVE") {
        sentimentData.Negative = 1;
    } else {
        sentimentData.Neutral = 1;
    }

    sentimentChart.data.datasets[0].data = [sentimentData.Positive, sentimentData.Negative, sentimentData.Neutral];
    sentimentChart.update();
}

// Update the intent box with the latest intent
function updateIntent(intent) {
    intentBox.textContent = intent ? `Latest Intent: ${intent}` : 'No intent detected';
}

// Start the bot
startBtn.addEventListener('click', () => {
    fetch('/start-bot')
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.message);
            fetchBotStatus(); // Start polling for bot's status
        })
        .catch(error => {
            console.error("Error starting bot:", error);
            addMessage('bot', "An error occurred while starting the bot.");
        });
});

// Stop the bot
stopBtn.addEventListener('click', () => {
    fetch('/stop-bot')
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.message);
            if (statusInterval) {
                clearInterval(statusInterval); // Stop polling if it's running
            }
        })
        .catch(error => {
            console.error("Error stopping bot:", error);
            addMessage('bot', "An error occurred while stopping the bot.");
        });
});

// Poll the bot's status to get real-time updates
function fetchBotStatus() {
    statusInterval = setInterval(() => {
        fetch('/status')
            .then(response => response.json())
            .then(data => {
                if (data.latest_bot_response) {
                    addMessage('bot', data.latest_bot_response);

                    if (data.sentiment_label) {
                        updateChart(data.sentiment_label); // Update sentiment chart
                    }

                    if (data.latest_intent) {
                        updateIntent(data.latest_intent); // Update intent box
                    }
                }
            })
            .catch(error => {
                console.error("Error fetching bot status:", error);
                addMessage('bot', "An error occurred while fetching the bot status.");
            });
    }, 2000); // Poll every 2 seconds
}

// Initialize the chart when the page loads
initializeChart();
