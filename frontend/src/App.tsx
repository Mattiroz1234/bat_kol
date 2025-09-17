import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import LoginForm from './components/LoginForm';
import ProfileForm from './components/ProfileForm';
import MatchesView from './components/MatchesView';
import ApiExplorer from './components/ApiExplorer';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasProfile, setHasProfile] = useState(false);
  const [userId, setUserId] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('userId');
    const storedHasProfile = localStorage.getItem('hasProfile');
    
    if (token && storedUserId) {
      setIsAuthenticated(true);
      setUserId(storedUserId);
      setHasProfile(storedHasProfile === 'true');
    }
    setLoading(false);
  }, []);

  const handleLoginSuccess = (token: string) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleProfileCreated = (personId: string) => {
    localStorage.setItem('userId', personId);
    localStorage.setItem('hasProfile', 'true');
    setUserId(personId);
    setHasProfile(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('hasProfile');
    setIsAuthenticated(false);
    setHasProfile(false);
    setUserId('');
  };

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Layout showHeader={false}>
        <LoginForm onLoginSuccess={handleLoginSuccess} />
      </Layout>
    );
  }

  if (!hasProfile) {
    return (
      <Layout title="יצירת פרופיל" onLogout={handleLogout}>
        <ProfileForm onProfileCreated={handleProfileCreated} />
      </Layout>
    );
  }

  return (
    <Router>
      <Layout title="פלטפורמת שידוכים" onLogout={handleLogout}>
        <Routes>
          <Route 
            path="/" 
            element={<MatchesView userId={userId} />} 
          />
          <Route path="/api-explorer" element={<ApiExplorer />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;