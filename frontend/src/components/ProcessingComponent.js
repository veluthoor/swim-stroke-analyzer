import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5001/api';

function ProcessingComponent({ videoId, onComplete }) {
  const [status, setStatus] = useState({ progress: 0, message: 'Starting analysis...' });
  const [error, setError] = useState(null);

  useEffect(() => {
    const pollStatus = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status/${videoId}`);
        const data = await response.json();

        if (response.ok) {
          setStatus(data);

          if (data.status === 'completed') {
            clearInterval(pollStatus);
            setTimeout(() => onComplete(), 1000);
          } else if (data.status === 'failed') {
            clearInterval(pollStatus);
            setError(data.error || 'Analysis failed. Please try again.');
          }
        }
      } catch (err) {
        console.error('Error polling status:', err);
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(pollStatus);
  }, [videoId, onComplete]);

  return (
    <div className="card">
      <h2 style={{ textAlign: 'center', marginBottom: '30px' }}>
        Analyzing Your Swim Technique...
      </h2>

      {!error && (
        <div className="progress-container">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${status.progress || 0}%` }}
            >
              {status.progress || 0}%
            </div>
          </div>
          <div className="status-message">
            {status.message || 'Processing...'}
          </div>
          <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <div className="loading-spinner"></div>
          </div>
        </div>
      )}

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="tips-section" style={{ marginTop: '30px' }}>
        <h4>What is happening?</h4>
        <ul>
          <li>🔍 Detecting body landmarks using AI</li>
          <li>📐 Calculating angles and positions</li>
          <li>📊 Analyzing technique metrics</li>
          <li>🎬 Creating annotated video</li>
          <li>📝 Generating personalized feedback</li>
        </ul>
        <p style={{ marginTop: '15px', color: '#666' }}>
          This usually takes 1-3 minutes depending on video length.
        </p>
      </div>
    </div>
  );
}

export default ProcessingComponent;
