function upload() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData
    }).then(res => res.json()).then(data => alert(data.message));
}

function summarize() {
    fetch("http://localhost:5000/summarize")
        .then(res => res.json())
        .then(data => {
            document.getElementById("summary").innerText = "Summary: " + data.summary;
        });
}

function ask() {
    const question = document.getElementById("question").value;
    fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("answer").innerText = "Answer: " + data.answer;
        });
}
