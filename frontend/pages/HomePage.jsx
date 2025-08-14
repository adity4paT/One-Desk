import React from 'react';
import FeatureCard from '../../components/FeatureCard';

const HomePage = ({ onNavigate }) => {
  const features = [
    {
      title: "HR Policy Search",
      description: "Upload documents and search for specific HR policies and procedures",
      icon: "🔍",
      path: "hr-policy"
    },
    {
      title: "Meeting Summarizer", 
      description: "Upload meeting recordings or transcripts to generate summaries and action items",
      icon: "📝",
      path: "meeting-summarizer"
    },
    {
      title: "Expense Tracker",
      description: "Track and categorize your business expenses with AI assistance",
      icon: "💰",
      path: "expense-tracker"
    },
    {
      title: "Resume Skill Updater",
      description: "Analyze job descriptions and update your resume with relevant skills",
      icon: "📄",
      path: "resume-updater"
    }
  ];

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl text-gray-800 font-bold mb-4">
          Welcome to OneDesk Mini Assistant
        </h1>
        <p className="text-xl text-gray-600">
          Your AI-powered workplace companion for enhanced productivity
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature, index) => (
          <div key={index}>
            <FeatureCard
              title={feature.title}
              description={feature.description}
              icon={feature.icon}
              onClick={() => onNavigate(feature.path)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
