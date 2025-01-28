const initialForm = document.getElementById("initial-form");
const mainContent = document.getElementById("main-content");
const userInfoForm = document.getElementById("user-info-form");
const viewToggle = document.getElementById("view-toggle");
const userView = document.getElementById("user-view");
const salespersonView = document.getElementById("salesperson-view");

// Toggle Switch Logic
viewToggle.addEventListener("change", () => {
  if (viewToggle.checked) {
    // Salesperson View
    userView.classList.add("hidden");
    salespersonView.classList.remove("hidden");
    document.getElementById("post-call-insights").classList.remove("hidden"); // Show Post-Call Insights
    document.getElementById("negotiation-coach").classList.remove("hidden"); // Show Negotiation Coach
  } else {
    // User View
    userView.classList.remove("hidden");
    salespersonView.classList.add("hidden");
    document.getElementById("post-call-insights").classList.add("hidden"); // Hide Post-Call Insights
    document.getElementById("negotiation-coach").classList.add("hidden"); // Hide Negotiation Coach
  }
});

document
  .getElementById("user-info-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    // Save user data to local storage
    localStorage.setItem("userName", name);
    localStorage.setItem("userEmail", email);

    // Check if the user is new or existing
    fetch("/get_response", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: "", // Empty input to trigger the check
        user_name: name,
        email: email,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Hide the initial form and show the main content
        document.getElementById("initial-form").classList.add("hidden");
        document.getElementById("main-content").classList.remove("hidden");

        // Display welcome message based on user status
        if (data.is_existing_user) {
          if (data.last_product) {
            showNotification(
              `👋 Welcome back, ${data.user_name}! Last time, you were looking for ${data.last_product}.`
            );
          } else {
            showNotification(`👋 Welcome back, ${data.user_name}!`);
          }
        } else {
          showNotification("🎉 Welcome to Sentimind AI!"); // Auto-dismissing notification for new users
          showNotification(
            "🌟 New user detected! We're excited to have you on board. Let's get started!"
          ); // Auto-dismissing pop-up
        }

        // Default to User View
        viewToggle.checked = false;
        userView.classList.remove("hidden");
        salespersonView.classList.add("hidden");
      })
      .catch((error) => {
        console.error("Error checking user status:", error);
      });
  });
// Rest of your existing JavaScript code for the main UI
const startRecordingBtn = document.getElementById("start-recording");
const stopRecordingBtn = document.getElementById("stop-recording");
const saveTranscriptBtn = document.getElementById("save-transcript");
const saveTranscriptSalesBtn = document.getElementById("save-transcript-sales");
const spokenText = document.getElementById("spoken-text");
const sentimentResult = document.getElementById("sentiment-result");
const emotionResult = document.getElementById("emotion-result");
const engagementBar = document.getElementById("engagement-bar");
const engagementFeedback = document.getElementById("engagement-feedback");
const purchaseIntent = document.getElementById("purchase-intent");
const behavioralIntent = document.getElementById("behavioral-intent");
const advancedIntent = document.getElementById("advanced-intent");
const suggestionsResult = document.getElementById("suggestions-result");
const transcriptionList = document.getElementById("transcription-list");
const negotiationTactics = document.getElementById("negotiation-tactics");
const objectionHandling = document.getElementById("objection-handling");

const recognition = new (window.SpeechRecognition ||
  window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.interimResults = false;
recognition.continuous = true;

let sentimentData = [];
let sentimentLabels = [];
let isRecording = false;
let transcriptionData = [];

const ctx = document.getElementById("sentiment-chart").getContext("2d");
const sentimentChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: sentimentLabels,
    datasets: [
      {
        label: "Sentiment Trend",
        data: sentimentData,
        borderColor: "#4CAF50",
        backgroundColor: "rgba(76, 175, 80, 0.2)",
        fill: true,
        lineTension: 0.2,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        min: -1,
        max: 1,
        ticks: {
          stepSize: 0.5,
        },
      },
      x: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
          lineWidth: 0.5,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      annotation: {
        annotations: {
          line0: {
            type: "line",
            yMin: 0,
            yMax: 0,
            borderColor: "#FF5722",
            borderWidth: 2,
            label: {
              enabled: false,
            },
          },
        },
      },
    },
  },
});

// Add this to your existing JavaScript in index.html
// Add this function to your JavaScript
function showNotification(message) {
  const notification = document.createElement("div");
  notification.className = "notification";
  notification.innerHTML = `
                <span>${message}</span>
            `;

  // Append the notification to the body
  document.body.appendChild(notification);

  // Automatically remove the notification after 4 seconds
  setTimeout(() => {
    notification.classList.add("fade-out");
    notification.addEventListener("animationend", () => {
      notification.remove();
    });
  }, 4000); // 4 seconds
}

recognition.onstart = () => {
  console.log("Recording started"); // Debugging
  isRecording = true;
  startRecordingBtn.classList.add("hidden");
  stopRecordingBtn.classList.remove("hidden");
  saveTranscriptBtn.classList.remove("hidden");
  saveTranscriptSalesBtn.classList.remove("hidden");
};

recognition.onend = () => {
  console.log("Recording stopped"); // Debugging
  isRecording = false;
  startRecordingBtn.classList.remove("hidden");
  stopRecordingBtn.classList.add("hidden");
  saveTranscriptBtn.classList.remove("hidden");
  saveTranscriptSalesBtn.classList.remove("hidden");

  // Generate post-call insights
  generatePostCallInsights();
};

recognition.onresult = (event) => {
  console.log("Speech recognized"); // Debugging
  const text = event.results[event.results.length - 1][0].transcript;

  // Retrieve user name from local storage
  const userName = localStorage.getItem("userName") || "You";

  // Update live transcription with user's name
  spokenText.textContent = `${userName} said: ${text}`;

  // Handle user input for coaching
  handleUserInputForCoaching(text);

  fetch("/get_response", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_input: text,
      user_name: localStorage.getItem("userName") || "You",
      email: localStorage.getItem("userEmail"),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const sentiment = data.sentiment;
      const emotion = data.emotion;
      const engagement = data.engagement;
      const purchase = data.purchase_intent;
      const behavioral = data.behavioral_intent;
      const advanced = data.advanced_intent;
      const suggestions = data.suggestions;
      const timestamp = new Date().toLocaleString();

      // Update sentiment, emotion, engagement, and intent results
      sentimentResult.textContent = `${sentiment}`;
      emotionResult.textContent = `${emotion}`;
      purchaseIntent.textContent = `Purchase Intent: ${purchase}`;
      behavioralIntent.textContent = `Behavioral Intent: ${behavioral}`;
      advancedIntent.textContent = `Advanced Intent: ${advanced}`;

      // Format recommendations with proper spacing and line breaks
      const formattedSuggestions = suggestions
        .split("\n") // Split by line breaks
        .map((line) => line.trim()) // Remove extra spaces
        .filter((line) => line.length > 0) // Remove empty lines
        .join("\n\n"); // Add double line breaks between recommendations

      suggestionsResult.textContent = formattedSuggestions;

      // Update sentiment chart
      let sentimentValue = 0;
      let sentimentColor = "#FF5722";
      if (sentiment === "Very Positive") {
        sentimentValue = 1;
        sentimentColor = "#4CAF50";
      } else if (sentiment === "Positive") {
        sentimentValue = 0.5;
        sentimentColor = "#8BC34A";
      } else if (sentiment === "Neutral") {
        sentimentValue = 0;
        sentimentColor = "#FF9800";
      } else if (sentiment === "Negative") {
        sentimentValue = -0.5;
        sentimentColor = "#F44336";
      } else if (sentiment === "Very Negative") {
        sentimentValue = -1;
        sentimentColor = "#D32F2F";
      }

      sentimentChart.data.datasets[0].borderColor = sentimentColor;
      sentimentChart.data.datasets[0].backgroundColor = `${sentimentColor}30`;

      sentimentData.push(sentimentValue);
      sentimentLabels.push(timestamp);
      sentimentChart.update();

      // Update engagement bar
      let engagementPercentage = 50;
      let engagementText = "Moderate engagement";

      if (sentiment === "Very Positive") {
        engagementPercentage = 100;
        engagementText = "High engagement";
      } else if (sentiment === "Positive") {
        engagementPercentage = 75;
        engagementText = "Moderate-to-High engagement";
      } else if (sentiment === "Neutral") {
        engagementPercentage = 50;
        engagementText = "Moderate engagement";
      } else if (sentiment === "Negative") {
        engagementPercentage = 25;
        engagementText = "Low engagement";
      } else if (sentiment === "Very Negative") {
        engagementPercentage = 10;
        engagementText = "Very Low engagement";
      }

      engagementBar.style.width = `${engagementPercentage}%`;
      engagementFeedback.textContent = engagementText;

      // Add transcription data to the list
      const listItem = document.createElement("li");
      listItem.textContent = `${timestamp}: ${userName} said: ${text}`;
      transcriptionList.appendChild(listItem);

      // Save transcription data for export
      transcriptionData.push({
        timestamp: timestamp,
        user_input: text,
        sentiment: sentiment,
        emotion: emotion,
        engagement: engagementText,
        purchase_intent: purchase,
        behavioral_intent: behavioral,
        advanced_intent: advanced,
        suggestions: suggestions,
      });
    });
};
recognition.onerror = (event) => {
  console.error("Speech recognition error:", event.error); // Debugging
};

startRecordingBtn.addEventListener("click", () => {
  console.log("Start Recording clicked"); // Debugging
  recognition.start();
});

stopRecordingBtn.addEventListener("click", () => {
  console.log("Stop Recording clicked"); // Debugging
  recognition.stop();
});

// Add this to your existing JavaScript code
const thumbsUpBtn = document.getElementById("thumbs-up");
const thumbsDownBtn = document.getElementById("thumbs-down");

thumbsUpBtn.addEventListener("click", () => handleFeedback("thumbs_up"));
thumbsDownBtn.addEventListener("click", () => handleFeedback("thumbs_down"));

const handleFeedback = async (feedback) => {
  try {
    // Get the current user input, email, and user name
    const userInput = spokenText.textContent.replace(
      `${localStorage.getItem("userName")} said: `,
      ""
    );
    const email = localStorage.getItem("userEmail");
    const userName = localStorage.getItem("userName") || "You";

    // Send feedback to the backend
    const response = await fetch("/handle_feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: userInput,
        email: email,
        feedback: feedback,
        user_name: userName, // Pass user_name to the backend
      }),
    });

    if (response.ok) {
      // Regenerate recommendations only for thumbs down
      if (feedback === "thumbs_down") {
        const data = await response.json();
        suggestionsResult.textContent = data.new_recommendations; // Preserve formatting
      } else {
        // For thumbs up, do not change recommendations
        alert("Thank you for your feedback!");
      }
    } else {
      console.error("Failed to send feedback");
    }
  } catch (error) {
    console.error("Error handling feedback:", error);
  }
};
// Save Transcript Functionality (for both User and Sales Views)
const saveTranscript = () => {
  const workbook = XLSX.utils.book_new();
  const worksheetData = [
    [
      "Date & Timestamp",
      "User Input",
      "Sentiment",
      "Emotional State",
      "Buyer Engagement",
      "Purchase Intent",
      "Behavioral Intent",
      "Advanced Intent",
      "Suggestions",
    ],
  ];

  transcriptionData.forEach((entry) => {
    worksheetData.push([
      entry.timestamp,
      entry.user_input,
      entry.sentiment,
      entry.emotion,
      entry.engagement,
      entry.purchase_intent,
      entry.behavioral_intent,
      entry.advanced_intent,
      entry.suggestions,
    ]);
  });

  const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
  XLSX.utils.book_append_sheet(workbook, worksheet, "Transcript");
  XLSX.writeFile(workbook, "transcript.xlsx");
};

saveTranscriptBtn.addEventListener("click", saveTranscript);
saveTranscriptSalesBtn.addEventListener("click", saveTranscript);

// Function to generate post-call insights
const generatePostCallInsights = async () => {
  try {
    // Combine all transcriptions into a single string
    const transcription = transcriptionData
      .map((entry) => entry.user_input)
      .join(" ");

    // Show loading spinner
    document.getElementById("loading-spinner").classList.remove("hidden");

    // Fetch insights from the backend
    const response = await fetch("/post_call_insights", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ transcription }),
    });

    const data = await response.json();

    // Hide loading spinner
    document.getElementById("loading-spinner").classList.add("hidden");

    // Display insights in the UI
    document.getElementById("call-summary").textContent = data.summary;
    document.getElementById("performance-analytics").textContent =
      data.performance_analytics;
    document.getElementById("deal-status").textContent = data.deal_status;
    document.getElementById("follow-up-suggestions").textContent =
      data.follow_up_suggestions;

    // Show the post-call insights section only in Salesperson View
    if (viewToggle.checked) {
      document.getElementById("post-call-insights").classList.remove("hidden");
    }
  } catch (error) {
    console.error("Error generating post-call insights:", error);
    alert("Failed to generate post-call insights. Please try again.");
  }
};

// Function to save insights as a file
const saveInsights = () => {
  const insights = {
    summary: document.getElementById("call-summary").textContent,
    performanceAnalytics: document.getElementById("performance-analytics")
      .textContent,
    dealStatus: document.getElementById("deal-status").textContent,
    followUpSuggestions: document.getElementById("follow-up-suggestions")
      .textContent,
  };

  // Convert insights to JSON
  const jsonData = JSON.stringify(insights, null, 2);

  // Create a Blob and download the file
  const blob = new Blob([jsonData], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "post_call_insights.json";
  a.click();
  URL.revokeObjectURL(url);
};

// Event listener for the "Save Insights" button
document
  .getElementById("save-insights")
  .addEventListener("click", saveInsights);

// Function to provide negotiation coaching
const provideNegotiationCoaching = async (user_input) => {
  try {
    // Show loading spinner
    document.getElementById("loading-spinner").classList.remove("hidden");

    // Fetch coaching suggestions from the backend
    const response = await fetch("/negotiation_coach", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input }),
    });

    const data = await response.json();

    // Hide loading spinner
    document.getElementById("loading-spinner").classList.add("hidden");

    // Display coaching suggestions in the UI
    negotiationTactics.textContent = data.negotiation_tactics;
    objectionHandling.textContent = data.objection_handling;

    // Show the negotiation coach section only in Salesperson View
    if (viewToggle.checked) {
      document.getElementById("negotiation-coach").classList.remove("hidden");
    }
  } catch (error) {
    console.error("Error providing negotiation coaching:", error);
    alert("Failed to provide negotiation coaching. Please try again.");
  }
};

// Function to handle user input for coaching
const handleUserInputForCoaching = (text) => {
  const coachingKeywords = ["price", "discount", "deal", "offer", "negotiate"];
  if (
    coachingKeywords.some((keyword) => text.toLowerCase().includes(keyword))
  ) {
    provideNegotiationCoaching(text);
  }
};
