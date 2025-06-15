import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import Week from './Week';
import EventForm from './EventForm';
import EventDetail from './EventDetail';
import { getTimeline, createEvent, getEvents } from '../services/api';

export default function Timeline() {
  const { currentUser } = useAuth();
  const [timeline, setTimeline] = useState([]);
  const [allEvents, setAllEvents] = useState([]);
  const [selectedWeek, setSelectedWeek] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showEventForm, setShowEventForm] = useState(false);
  const [showEventDetail, setShowEventDetail] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (currentUser) {
      loadTimeline();
      loadAllEvents();
    }
  }, [currentUser]);

  const loadTimeline = async () => {
    try {
      const response = await getTimeline();
      const data = response.data;
      
      const timelineWithDates = data.weeks.map(week => ({
        ...week,
        start_date: new Date(week.start_date),
        end_date: new Date(week.end_date),
        events: week.events.map(event => ({
          ...event,
          date: new Date(event.date)
        }))
      }));
      
      setTimeline(timelineWithDates);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load timeline", error);
      setError("Failed to load timeline. Please try again.");
      setLoading(false);
    }
  };

  const loadAllEvents = async () => {
    try {
      const response = await getEvents();
      setAllEvents(response.data);
    } catch (error) {
      console.error("Failed to load events", error);
    }
  };

  const handleWeekClick = (week) => {
    setSelectedWeek(week);
    setShowEventForm(true);
  };

  const handleEventClick = (event) => {
    setSelectedEvent(event);
    setShowEventDetail(true);
  };

  const handleAddEvent = async (eventData) => {
    try {
      await createEvent({
        ...eventData,
        date: selectedWeek.start_date.toISOString().split('T')[0]
      });
      loadTimeline();
      loadAllEvents();
      setShowEventForm(false);
    } catch (error) {
      console.error("Failed to add event", error);
    }
  };

  const handleUpdateEvent = (updatedEvent) => {
    // Update timeline
    const updatedTimeline = timeline.map(week => {
      const updatedEvents = week.events.map(event => 
        event.id === updatedEvent.id ? {...event, ...updatedEvent} : event
      );
      return {...week, events: updatedEvents};
    });
    
    setTimeline(updatedTimeline);
    
    // Update all events list
    const updatedAllEvents = allEvents.map(event => 
      event.id === updatedEvent.id ? updatedEvent : event
    );
    
    setAllEvents(updatedAllEvents);
    setSelectedEvent(updatedEvent);
  };

  const handleDeleteEvent = (deletedEventId) => {
    // Update timeline
    const updatedTimeline = timeline.map(week => ({
      ...week,
      events: week.events.filter(event => event.id !== deletedEventId)
    }));
    
    setTimeline(updatedTimeline);
    
    // Update all events list
    const updatedAllEvents = allEvents.filter(event => event.id !== deletedEventId);
    setAllEvents(updatedAllEvents);
    
    setShowEventDetail(false);
    setSelectedEvent(null);
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (loading) {
    return <div>Loading timeline...</div>;
  }

  // Group weeks by year
  const years = {};
  timeline.forEach(week => {
    const year = week.start_date.getFullYear();
    if (!years[year]) years[year] = [];
    years[year].push(week);
  });

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <h2>Your Life in Weeks</h2>
        <div className="event-stats">
          <span>Total Events: {allEvents.length}</span>
        </div>
      </div>
      
      <div className="years-grid">
        {Object.entries(years).map(([year, weeks]) => (
          <div key={year} className="year-row">
            <div className="year-label">{year}</div>
            <div className="weeks-container">
              {weeks.map(week => (
                <Week 
                  key={week.week_number} 
                  week={week} 
                  onClick={() => handleWeekClick(week)}
                  onEventClick={handleEventClick}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {showEventForm && selectedWeek && (
        <EventForm 
          week={selectedWeek}
          onSubmit={handleAddEvent}
          onCancel={() => setShowEventForm(false)}
        />
      )}
      
      {showEventDetail && selectedEvent && (
        <EventDetail 
          event={selectedEvent}
          onClose={() => setShowEventDetail(false)}
          onUpdate={handleUpdateEvent}
          onDelete={handleDeleteEvent}
        />
      )}
    </div>
  );
}