import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import HRPolicySearch from './pages/HRPolicySearch';
import MeetingSummarizer from './pages/MeetingSummarizer';
import ExpenseTracker from './pages/ExpenseTracker';
import ResumeSkillUpdater from './pages/ResumeSkillUpdater';
import './App.css';

const App = () => {
  const [currentPage, setCurrentPage] = useState('home');

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'hr-policy':
        return <HRPolicySearch />;
      case 'meeting-summarizer':
        return <MeetingSummarizer />;
      case 'expense-tracker':
        return <ExpenseTracker />;
      case 'resume-updater':
        return <ResumeSkillUpdater />;
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <header className="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
        <div className="max-w-6xl mx-auto px-8 py-4">
          <h1 
            className="text-blue-600 cursor-pointer text-2xl font-semibold transition-colors duration-200 hover:text-blue-700"
            onClick={() => handleNavigate('home')}
          >
            OneDesk Mini Assistant
          </h1>
        </div>
      </header>
      <main className="pt-20">
        {renderCurrentPage()}
      </main>
    </div>
  );
};

export default App;
