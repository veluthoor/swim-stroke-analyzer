import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5001/api';

function ResultsComponent({ videoId, onReset }) {
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReport();
  }, [videoId]);

  const fetchReport = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/result/${videoId}/report`);
      const data = await response.json();

      if (response.ok) {
        setReport(data.report);
      } else {
        setError('Failed to load report');
      }
    } catch (err) {
      setError('Network error loading report');
    } finally {
      setLoading(false);
    }
  };

  const videoUrl = `${API_BASE_URL}/result/${videoId}/video`;

  return (
    <div>
      <div className="card">
        <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#667eea' }}>
          ✅ Analysis Complete!
        </h2>

        <div className="video-container">
          <div className="video-wrapper">
            <h3>Analyzed Video with Feedback</h3>
            <video controls style={{ width: '100%' }}>
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>

        <div style={{ textAlign: 'center', margin: '20px 0' }}>
          <a
            href={videoUrl}
            download
            className="button"
            style={{ marginRight: '10px', textDecoration: 'none', display: 'inline-block' }}
          >
            📥 Download Video
          </a>
          <button className="button" onClick={onReset}>
            🔄 Analyze Another Video
          </button>
        </div>
      </div>

      <div className="card">
        <div className="report-section">
          <h2>📊 Detailed Analysis Report</h2>
          {loading && (
            <div style={{ textAlign: 'center' }}>
              <div className="loading-spinner"></div>
              <p>Loading report...</p>
            </div>
          )}
          {error && (
            <div className="error-message">{error}</div>
          )}
          {!loading && !error && (
            <div className="report-content">{report}</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResultsComponent;
