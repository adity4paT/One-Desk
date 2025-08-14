import React from 'react';
import ReusableButton from './ReusableButton';

const FeatureCard = ({ title, description, icon, onClick }) => {
  return (
    <div 
      className="bg-white rounded-xl shadow-md p-6 cursor-pointer transition-all duration-200 h-full flex flex-col hover:shadow-lg hover:-translate-y-1"
      onClick={onClick}
    >
      <div className="flex-grow text-center">
        <div className="text-5xl mb-4">{icon}</div>
        <h3 className="text-xl text-gray-800 font-medium mb-2">{title}</h3>
        <p className="text-gray-600 leading-relaxed">{description}</p>
      </div>
      <div className="mt-4 text-center">
        <ReusableButton variant="outlined" size="small">
          Get Started →
        </ReusableButton>
      </div>
    </div>
  );
};

export default FeatureCard;
