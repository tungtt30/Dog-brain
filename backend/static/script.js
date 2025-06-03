
let documentLoaded = false;

function showMessage(message, isError = false) {
    const answerDiv = document.getElementById("answer");
    answerDiv.innerText = message;
    answerDiv.style.color = isError ? "#ff6b6b" : "#333";
}

function showLoading(show = true) {
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => btn.disabled = show);

    if (show) {
        showMessage("Processing...");
    }
}

async function upload() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        showMessage("Please choose file!", true);
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoading(true);

    try {
        const response = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            documentLoaded = true;
            showMessage(`✅ ${data.message}\nLength: ${data.content_length} tokens`);

            // Enable ask button
            const askButton = document.getElementById("askButton");
            if (askButton) askButton.disabled = false;

        } else {
            showMessage(`❌ ${data.error}`, true);
        }
    } catch (error) {
        showMessage(`❌ Connection error: ${error.message}`, true);
    } finally {
        showLoading(false);
    }
}

async function translat() {
    const question = document.getElementById("question").value.trim();

    if (!question) {
        showMessage("Please type text!", true);
        return;
    }

    showLoading(true);

    try {
        const response = await fetch("http://localhost:5000/trans", {
            method: "POST",
            headers: { 'Content-Type': 'application/json; charset=UTF-8' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(`🌐 Trans:\n${data.answer}`);
        } else {
            showMessage(`❌ ${data.error}`, true);
        }
    } catch (error) {
        showMessage(`❌ Connection error: ${error.message}`, true);
    } finally {
        showLoading(false);
    }
}

async function summarize() {
    if (!documentLoaded) {
        showMessage("Please upload document first!", true);
        return;
    }

    showLoading(true);

    try {
        const response = await fetch("http://localhost:5000/summ", {
            method: "POST",
            headers: { 'Content-Type': 'application/json; charset=UTF-8' },
            body: JSON.stringify({ question: "" })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(`📄 Summerize:\n${data.answer}`);
        } else {
            showMessage(`❌ ${data.error}`, true);
        }
    } catch (error) {
        showMessage(`❌ Connection error: ${error.message}`, true);
    } finally {
        showLoading(false);
    }
}

async function ask() {
    const question = document.getElementById("question").value.trim();

    if (!question) {
        showMessage("Input question!", true);
        return;
    }

    if (!documentLoaded) {
        showMessage("Upload first!", true);
        return;
    }

    showLoading(true);

    try {
        const response = await fetch("http://localhost:5000/ask", {
            method: "POST",
            headers: { 'Content-Type': 'application/json; charset=UTF-8' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(`🤖 Ans:\n${data.answer}`);
        } else {
            showMessage(`❌ ${data.error}`, true);
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, true);
    } finally {
        showLoading(false);
    }
}


window.onload = async function () {
    try {
        const response = await fetch("http://localhost:5000/status");
        const data = await response.json();
        documentLoaded = data.document_loaded;

        if (documentLoaded) {
            showMessage(`📄 Uploaded (${data.document_length} ký tự)`);
        } else {
            showMessage("Not uploaded yet, Please check");
        }
    } catch (error) {
        showMessage("Server error", true);
    }
};

// Enter
document.addEventListener('DOMContentLoaded', function () {
    const questionInput = document.getElementById("question");
    questionInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            ask();
        }
    });
});