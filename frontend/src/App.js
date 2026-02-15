import React, { useState } from 'react';
import './App.css';
import UploadComponent from './components/UploadComponent';
import ProcessingComponent from './components/ProcessingComponent';
import ResultsComponent from './components/ResultsComponent';

function App() {
  const [stage, setStage] = useState('upload'); // upload, processing, results
  const [videoId, setVideoId] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelected = (file) => {
    setSelectedFile(file);
  };

  const handleUploadComplete = (id) => {
    setVideoId(id);
    setStage('processing');
  };

  const handleProcessingComplete = () => {
    setStage('results');
  };

  const handleReset = () => {
    setStage('upload');
    setVideoId(null);
    setSelectedFile(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header" style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white'
        }}>
          <h1 style={{ color: 'white' }}>🏊‍♂️ Swim Stroke Analyzer</h1>
          <p style={{ color: 'rgba(255,255,255,0.95)', fontSize: '1.15rem' }}>
            AI-powered freestyle coach in your pocket. Upload, analyze, improve! 🚀
          </p>
        </header>

        {stage === 'upload' && (
          <UploadComponent
            onFileSelected={handleFileSelected}
            onUploadComplete={handleUploadComplete}
            selectedFile={selectedFile}
          />
        )}

        {stage === 'processing' && (
          <ProcessingComponent
            videoId={videoId}
            onComplete={handleProcessingComplete}
          />
        )}

        {stage === 'results' && (
          <ResultsComponent
            videoId={videoId}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  );
}

export default App;
