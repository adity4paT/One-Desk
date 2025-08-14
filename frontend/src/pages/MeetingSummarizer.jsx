import React, { useState } from 'react';
import FileUploadSection from '../components/FileUploadSection';
import ReusableButton from '../components/ReusableButton';
import ResultCard from '../components/ResultCard';

const MeetingSummarizer = () => {
  const [tabValue, setTabValue] = useState(0);
  const [hasResults, setHasResults] = useState(false);

  const handleFileUpload = (file) => {
    console.log('File uploaded for Meeting Summarizer:', file);
  };

  const handleSummarize = () => {
    console.log('Generating meeting summary...');
    setHasResults(true);
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl text-gray-800 font-bold mb-2">
          Meeting Summarizer
        </h1>
        <p className="text-xl text-gray-600">
          Upload meeting recordings or transcripts to generate AI-powered summaries
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div>
          <FileUploadSection
            onFileUpload={handleFileUpload}
            acceptedTypes=".mp3,.mp4,.wav,.txt,.pdf"
            label="Upload Meeting File"
          />
        </div>
        <div className="flex items-center h-full">
          <ReusableButton
            onClick={handleSummarize}
            fullWidth
            size="large"
            startIcon="📝"
          >
            Generate Summary
          </ReusableButton>
        </div>
      </div>
      {hasResults && (
        <div className="mt-12">
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="flex border-b border-gray-200">
              <button 
                className={`flex-1 p-4 text-base font-medium transition-all duration-200 ${
                  tabValue === 0 
                    ? 'text-blue-600 bg-blue-50' 
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
                onClick={() => setTabValue(0)}
              >
                Summary
              </button>
              <button 
                className={`flex-1 p-4 text-base font-medium transition-all duration-200 ${
                  tabValue === 1 
                    ? 'text-blue-600 bg-blue-50' 
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
                onClick={() => setTabValue(1)}
              >
                Action Items
              </button>
            </div>
            <div className="p-8">
              {tabValue === 0 && (
                <div>
                  <p className="text-gray-600 mb-4 leading-relaxed">
                    Meeting summary will appear here after processing...
                  </p>
                  <ResultCard
                    title="Key Discussion Points"
                    content="The team discussed the Q4 roadmap, budget allocation, and upcoming product launches. Main focus was on improving user experience and expanding market reach."
                  />
                </div>
              )}
              {tabValue === 1 && (
                <div>
                  <p className="text-gray-600 mb-4 leading-relaxed">
                    Action items extracted from the meeting:
                  </p>
                  <ResultCard
                    title="Action Item 1"
                    content="John to prepare Q4 budget proposal by Friday"
                  />
                  <ResultCard
                    title="Action Item 2" 
                    content="Sarah to schedule follow-up meeting with design team"
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MeetingSummarizer;
