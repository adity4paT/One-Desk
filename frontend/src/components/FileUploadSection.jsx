import React, { useState } from 'react';

const FileUploadSection = ({ onFileUpload, acceptedTypes = "*/*", label = "Upload File" }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    onFileUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    setSelectedFile(file);
    onFileUpload(file);
  };

  return (
    <div 
      className={`bg-gray-50 border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
        isDragging ? 'border-blue-600 bg-gray-100' : 'border-gray-300 hover:border-blue-600 hover:bg-gray-100'
      }`}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onDragEnter={() => setIsDragging(true)}
      onDragLeave={() => setIsDragging(false)}
    >
      <input
        type="file"
        accept={acceptedTypes}
        onChange={handleFileChange}
        className="hidden"
        id="file-upload"
      />
      <label htmlFor="file-upload" className="block cursor-pointer">
        <div className="text-5xl mb-4">📁</div>
        <h3 className="text-gray-800 text-lg font-medium mb-2">{label}</h3>
        {selectedFile ? (
          <div className="mt-2">
            <span className="bg-blue-50 text-blue-600 px-4 py-2 rounded-full border border-blue-200 inline-block">
              {selectedFile.name}
            </span>
          </div>
        ) : (
          <p className="text-gray-600">Click to browse or drag and drop</p>
        )}
      </label>
    </div>
  );
};

export default FileUploadSection;
