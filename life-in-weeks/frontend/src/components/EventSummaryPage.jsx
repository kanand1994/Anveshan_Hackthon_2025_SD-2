import React from 'react';
import EventSummary from './EventSummary';
import Header from './Header';
import { useAuth } from '../context/AuthContext';

export default function EventSummaryPage() {
  const { currentUser } = useAuth();

  return (
    <div className="app">
      <Header />
      <main>
        {currentUser ? <EventSummary /> : <div>Please log in to view event summary</div>}
      </main>
    </div>
  );
}