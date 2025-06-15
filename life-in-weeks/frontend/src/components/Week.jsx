import React from 'react';
import { format } from 'date-fns';

export default function Week({ week, onClick, onEventClick }) {
  const hasEvents = week.events && week.events.length > 0;
  const weekClass = `week-box ${hasEvents ? 'has-events' : ''}`;
  
  // Format week range for tooltip
  const weekRange = `${format(week.start_date, 'MMM d')} - ${format(week.end_date, 'MMM d, yyyy')}`;
  
  return (
    <div 
      className={weekClass}
      title={`Week ${week.week_number}: ${weekRange}`}
    >
      {hasEvents && (
        <div className="events-container">
          {week.events.map(event => (
            <div 
              key={event.id} 
              className="event-indicator"
              title={`${event.title}\n${format(new Date(event.date), 'MMM d, yyyy')}`}
              onClick={(e) => {
                e.stopPropagation();
                onEventClick(event);
              }}
            >
              {event.title.substring(0, 1)}
            </div>
          ))}
        </div>
      )}
      
      <div className="week-background" onClick={onClick}></div>
    </div>
  );
}