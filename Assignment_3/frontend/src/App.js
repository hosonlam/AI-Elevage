import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import axios from "axios";
import "./App.css";

function TranscriptSummarizer() {
  const [file, setFile] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setFile(file);
  };

  const handleSummarize = async () => {
    if (!file) return;
    setIsLoading(true);

    console.log("File to upload:", file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      setIsLoading(false);
      setSummary(res.data.content);
    } catch (error) {}
  };

  return (
    <div
      style={{
        width: 1024,
        margin: "2rem auto",
        padding: "2rem",
        border: "1px solid #ccc",
        borderRadius: 8,
      }}
    >
      <h2 style={{ marginTop: 0 }}>Transcript Summarizer</h2>
      <section
        style={{
          marginBottom: "1rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <label style={{ marginRight: "24px" }}>
          <strong>Upload transcript text file:</strong>
        </label>
        <input type="file" accept=".txt" onChange={handleFileUpload} />
      </section>
      <button
        onClick={handleSummarize}
        disabled={!file}
        style={{
          marginBottom: "1rem",
          width: 200,
          height: 48,
          fontSize: "16px",
          background: "darkorange",
          fontWeight: 800,
          color: "black",
          borderRadius: 8,
        }}
      >
        Start Summarizer
      </button>
      {isLoading && (
        <div
          style={{
            marginBottom: "1rem",
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 12,
          }}
        >
          <div
            style={{
              width: 24,
              height: 24,
              border: "4px solid #ccc",
              borderTop: "4px solid darkorange",
              borderRadius: "50%",
              animation: "spin 1s linear infinite",
            }}
          />
          Summarizing, please wait...
          <style>
            {`
              @keyframes spin {
                0% { transform: rotate(0deg);}
                100% { transform: rotate(360deg);}
              }
            `}
          </style>
        </div>
      )}
      {summary && !isLoading && (
        <section>
          <strong>Output:</strong>
          <div
            style={{
              minHeight: 200,
              maxHeight: 400,
              marginTop: 8,
              background: "#f9f9f9",
              padding: 8,
              paddingLeft: 24,
              paddingRight: 24,
              borderRadius: 4,
              color: "black",
              textAlign: "left",
              overflowY: "auto",
            }}
          >
            <ReactMarkdown>{summary}</ReactMarkdown>
          </div>
        </section>
      )}
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <TranscriptSummarizer />
      </header>
    </div>
  );
}

export default App;
