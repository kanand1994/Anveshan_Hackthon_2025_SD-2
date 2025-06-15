import React, { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Timeline from './components/Timeline';
import EventSummaryPage from './components/EventSummaryPage';
import Header from './components/Header';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './index.css';
import Auth from './components/Auth';
import EventSummary from './components/EventSummary';

function App() {
  const { currentUser } = useContext(AuthContext);

  return (
    <Router>
      <div className="app">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={currentUser ? <Timeline /> : <Navigate to="/login" />} />
            <Route path="/events" element={currentUser ? <EventSummaryPage /> : <Navigate to="/login" />} />
            <Route path="/login" element={!currentUser ? <Auth /> : <Navigate to="/" />} />
			<Route path="/summary" element={<EventSummary />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;