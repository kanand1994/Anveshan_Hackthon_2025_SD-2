import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getEventsSummary, restoreEvent } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './EventSummary.css';

export default function EventSummary() {
  const { currentUser } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (currentUser) {
      loadEventSummary();
    }
  }, [currentUser]);

  const loadEventSummary = async () => {
    try {
      setLoading(true);
      const response = await getEventsSummary();
      setSummary(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load event summary", error);
      setError("Failed to load event summary. Please try again.");
      setLoading(false);
    }
  };

  const handleRestore = async (eventId) => {
    try {
      await restoreEvent(eventId);
      loadEventSummary();
    } catch (error) {
      console.error("Failed to restore event", error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const renderEventList = (events, title, showRestore = false) => {
    if (!events || events.length === 0) {
      return <p>No {title.toLowerCase()} events</p>;
    }

    return (
      <div className="event-section">
        <h3>{title} Events ({events.length})</h3>
        <div className="event-list">
          {events.map(event => (
            <div key={event.id} className={`event-card ${event.deleted_at ? 'deleted' : ''}`}>
              <div className="event-header">
                <h4>{event.title}</h4>
                <span className="event-date">{formatDate(event.date)}</span>
              </div>
              <div className="event-category">
                Category: <span className="category-tag">{event.category}</span>
              </div>
              {event.description && (
                <p className="event-description">{event.description}</p>
              )}
              {event.deleted_at && showRestore && (
                <div className="event-actions">
                  <button 
                    className="restore-button"
                    onClick={() => handleRestore(event.id)}
                  >
                    Restore Event
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) return <div>Loading event summary...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="event-summary">
      <div className="summary-header">
        <h2>Event Summary</h2>
        <button onClick={loadEventSummary}>Refresh</button>
      </div>

      {summary && (
        <>
          {renderEventList(summary.present, "Present")}
          {renderEventList(summary.future, "Future")}
          {renderEventList(summary.past, "Past")}
          {renderEventList(summary.deleted, "Deleted", true)}
        </>
      )}
    </div>
  );
  const EventSummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [debugInfo, setDebugInfo] = useState('');
  
  // Get token from storage
  const token = localStorage.getItem('token');
  
  // Set default date range (current year)
  const currentYear = new Date().getFullYear();
  const [startDate, setStartDate] = useState(`${currentYear}-01-01`);
  const [endDate, setEndDate] = useState(`${currentYear}-12-31`);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        setLoading(true);
        setError('');
        setDebugInfo('');
        
		console.log("Sending request with params:", {
			start_date: startDate,
			end_date: endDate
		});
        // Create URL with properly encoded parameters
        const params = new URLSearchParams({
          start_date: startDate,
          end_date: endDate
        });
        
        const url = `/events/summary?${params.toString()}`;
        
        // Add debug info (FIXED TERNARY OPERATOR)
        setDebugInfo(`URL: ${url}\nToken: ${token ? token.substring(0, 20) : ''}...`);
        
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (!response.ok) {
          let errorText = await response.text();
          try {
            const errorJson = JSON.parse(errorText);
            errorText = errorJson.detail || errorJson.message || errorText;
          } catch {
            // Not JSON
          }
          
          throw new Error(`HTTP Error ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        setSummary(data);
      } catch (err) {
        setError(`Failed to load event summary: ${err.message}`);
        console.error('Event summary error:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchSummary();
  }, [token, startDate, endDate]);

  const handleRetry = () => {
    setError('');
    setLoading(true);
    setTimeout(() => {
      const fetchSummary = async () => {
        try {
          const params = new URLSearchParams({
            start_date: startDate,
            end_date: endDate
          });
          
          const response = await fetch(
            `/events/summary?${params.toString()}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            }
          );
          
          if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
          
          const data = await response.json();
          setSummary(data);
          setError('');
        } catch (err) {
          setError(`Retry failed: ${err.message}`);
        } finally {
          setLoading(false);
        }
      };
      
      fetchSummary();
    }, 1000);
  };

  return (
    <div className="event-summary">
      <h2>Event Summary</h2>
      
      <div className="date-controls">
        <label>
          Start Date:
          <input 
            type="date" 
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        
        <label>
          End Date:
          <input 
            type="date" 
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
      </div>
      
      {loading && <div className="loading-indicator">Loading summary...</div>}
      
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={handleRetry} className="retry-button">
            Try Again
          </button>
          <div className="debug-info">
            <h4>Debug Information:</h4>
            <pre>{debugInfo}</pre>
            <p>Current token: {token ? token.substring(0, 20) + '...' : 'No token found'}</p>
          </div>
        </div>
      )}
      
      {summary && !error && !loading && (
        <div className="summary-data">
          <p>Total Events: {summary.total_events}</p>
          <p>Earliest Event: {summary.earliest_event || 'None'}</p>
          <p>Latest Event: {summary.latest_event || 'None'}</p>
          
          <h3>By Category:</h3>
          <ul>
            {Object.entries(summary.categories).map(([category, count]) => (
              <li key={category}>
                {category}: {count}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};



}