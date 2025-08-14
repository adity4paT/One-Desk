import React, { useState } from 'react';
import FileUploadSection from '../../components/FileUploadSection';
import ReusableButton from '../../components/ReusableButton';
import ResultCard from '../../components/ResultCard';

const HRPolicySearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleFileUpload = (file) => {
    console.log('File uploaded for HR Policy Search:', file);
  };

  const handleSearch = () => {
    console.log('Searching for:', query);
    setResults([
      {
        title: "Remote Work Policy",
        content: "Found relevant information about remote work guidelines and requirements..."
      },
      {
        title: "Leave Policy", 
        content: "Details about vacation days, sick leave, and other time-off policies..."
      }
    ]);
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl text-gray-800 font-bold mb-2">
          HR Policy Search
        </h1>
        <p className="text-xl text-gray-600">
          Upload documents and search for specific HR policies
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div>
          <FileUploadSection
            onFileUpload={handleFileUpload}
            acceptedTypes=".pdf,.doc,.docx,.txt"
            label="Upload HR Documents"
          />
        </div>
        <div className="flex flex-col gap-4 justify-center">
          <textarea
            className="w-full p-4 border border-gray-300 rounded-lg text-base resize-vertical focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="e.g., What is the remote work policy?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={4}
          />
          <ReusableButton
            onClick={handleSearch}
            disabled={!query.trim()}
            fullWidth
            startIcon="🔍"
          >
            Search Policies
          </ReusableButton>
        </div>
      </div>
      {results.length > 0 && (
        <div className="mt-12">
          <h2 className="text-gray-800 text-2xl font-bold mb-6">Search Results</h2>
          {results.map((result, index) => (
            <ResultCard
              key={index}
              title={result.title}
              content={result.content}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default HRPolicySearch;
