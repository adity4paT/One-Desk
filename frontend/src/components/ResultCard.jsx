import React from 'react';

const ResultCard = ({ title, content, actions }) => (
  <div className="bg-white rounded-xl shadow-md mb-4 overflow-hidden">
    <div className="p-6">
      <h3 className="text-gray-800 text-lg font-medium mb-2">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{content}</p>
    </div>
    {actions && (
      <div className="px-6 pb-6">
        {actions}
      </div>
    )}
  </div>
);

export default ResultCard;
