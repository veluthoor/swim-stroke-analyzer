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
    <div className="card">
      <div
        className={`upload-area ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
      >
        <div className="upload-icon">📹</div>
        <div className="upload-text">
          <h3>Upload Your Swimming Video</h3>
          <p>Drag and drop your video here, or click to browse</p>
          <p style={{ fontSize: '0.9rem', color: '#999' }}>
            Supported formats: MP4, AVI, MOV (max 500MB)
          </p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="video/mp4,video/avi,video/quicktime"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>

      {selectedFile && (
        <div className="file-info">
          <p><strong>Selected File:</strong> {selectedFile.name}</p>
          <p><strong>Size:</strong> {formatFileSize(selectedFile.size)}</p>
          <p><strong>Type:</strong> {selectedFile.type}</p>
          <button
            className="button"
            onClick={handleUpload}
            disabled={uploading}
            style={{ marginTop: '15px' }}
          >
            {uploading ? 'Uploading...' : 'Upload and Analyze'}
          </button>
        </div>
      )}

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="tips-section">
        <h4>💡 Tips for Best Results</h4>
        <ul>
          <li>Film from the side at pool deck level</li>
          <li>Keep the camera steady (use a tripod if possible)</li>
          <li>Ensure good lighting - outdoor pools in daylight work great</li>
          <li>Capture at least 2-3 complete stroke cycles</li>
          <li>Show the full body when possible</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadComponent;
