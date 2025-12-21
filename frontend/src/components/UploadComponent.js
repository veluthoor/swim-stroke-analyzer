import React, { useState, useRef } from 'react';

const API_BASE_URL = 'http://localhost:5001/api';

function UploadComponent({ onFileSelected, onUploadComplete, selectedFile }) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && isValidFile(file)) {
      onFileSelected(file);
      setError(null);
    } else {
      setError('Please upload a valid video file (MP4, AVI, or MOV)');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && isValidFile(file)) {
      onFileSelected(file);
      setError(null);
    } else {
      setError('Please upload a valid video file (MP4, AVI, or MOV)');
    }
  };

  const isValidFile = (file) => {
    const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo'];
    return validTypes.includes(file.type) || /\.(mp4|avi|mov)$/i.test(file.name);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        onUploadComplete(data.video_id);
      } else {
        setError(data.error || 'Upload failed. Please try again.');
        setUploading(false);
      }
    } catch (err) {
      setError('Network error. Please ensure the backend server is running.');
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <div>
      <div className="card">
        <div
          className={`upload-area ${dragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
          style={{
            background: dragging ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '',
            color: dragging ? 'white' : '',
            transition: 'all 0.3s ease'
          }}
        >
          <div className="upload-icon" style={{ fontSize: dragging ? '5rem' : '4rem', transition: 'all 0.3s ease' }}>
            {dragging ? '🎯' : '📹'}
          </div>
          <div className="upload-text">
            <h3 style={{ color: dragging ? 'white' : '' }}>
              {dragging ? 'Drop it like it\'s hot!' : 'Drop Your Swim Video Here'}
            </h3>
            <p style={{ color: dragging ? 'rgba(255,255,255,0.9)' : '' }}>
              {dragging ? 'Let go to upload' : 'Drag & drop or click to browse'}
            </p>
            {!dragging && (
              <p style={{ fontSize: '0.9rem', color: '#999', marginTop: '10px' }}>
                MP4, AVI, MOV • Max 500MB
              </p>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/mp4,video/avi,video/quicktime"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>

        {selectedFile && !uploading && (
          <div style={{
            background: 'linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%)',
            borderRadius: '12px',
            padding: '25px',
            marginTop: '25px',
            border: '2px solid #667eea'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
              <div style={{ fontSize: '2.5rem', marginRight: '15px' }}>✅</div>
              <div style={{ flex: 1 }}>
                <p style={{ margin: '0 0 5px 0', fontSize: '1.1rem', fontWeight: 'bold', color: '#333' }}>
                  {selectedFile.name}
                </p>
                <p style={{ margin: 0, fontSize: '0.95rem', color: '#666' }}>
                  {formatFileSize(selectedFile.size)} • {selectedFile.type || 'Video file'}
                </p>
              </div>
            </div>
            <button
              className="button"
              onClick={handleUpload}
              style={{
                width: '100%',
                fontSize: '1.2rem',
                padding: '15px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                transform: 'scale(1)',
                transition: 'transform 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.transform = 'scale(1.02)'}
              onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
            >
              🚀 Analyze My Swim!
            </button>
          </div>
        )}

        {error && (
          <div style={{
            background: '#FFF3F3',
            border: '2px solid #D32F2F',
            borderRadius: '12px',
            padding: '20px',
            marginTop: '20px',
            color: '#D32F2F',
            display: 'flex',
            alignItems: 'center'
          }}>
            <div style={{ fontSize: '2rem', marginRight: '15px' }}>⚠️</div>
            <div>
              <strong>Oops!</strong> {error}
            </div>
          </div>
        )}
      </div>

      <div style={{
        background: 'linear-gradient(135deg, #FFF9E6 0%, #FFF3E0 100%)',
        borderRadius: '16px',
        padding: '25px',
        marginTop: '20px',
        border: '2px solid #FFAB00'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
          <div style={{ fontSize: '2rem', marginRight: '10px' }}>💡</div>
          <h4 style={{ margin: 0, fontSize: '1.3rem', color: '#F57C00' }}>
            Pro Tips for Best Results
          </h4>
        </div>
        <ul style={{ margin: '10px 0', paddingLeft: '45px', lineHeight: '1.8' }}>
          <li><strong>Side angle</strong> - Film from the side at pool deck level</li>
          <li><strong>Keep it steady</strong> - Use a tripod or rest your phone on something</li>
          <li><strong>Good lighting</strong> - Outdoor daylight is perfect</li>
          <li><strong>Multiple strokes</strong> - Capture at least 2-3 complete cycles</li>
          <li><strong>Full body</strong> - Make sure your whole body is visible</li>
        </ul>
        <div style={{
          background: 'rgba(255,255,255,0.7)',
          borderRadius: '8px',
          padding: '15px',
          marginTop: '15px',
          fontSize: '0.95rem',
          color: '#666'
        }}>
          <strong>🎥 Quick tip:</strong> 10-15 seconds of footage is plenty. No need for a full lap!
        </div>
      </div>
    </div>
  );
}

export default UploadComponent;
