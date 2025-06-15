import React, { useState } from 'react';
import { format } from 'date-fns';
import { updateEvent, deleteEvent } from '../services/api';

export default function EventDetail({ event, onClose, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [eventData, setEventData] = useState({ ...event });
  
  const handleEditClick = () => {
    setIsEditing(true);
  };
  
  const handleSave = async () => {
    try {
      const updatedEvent = await updateEvent(event.id, eventData);
      onUpdate(updatedEvent.data);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update event", error);
    }
  };
  
  const handleDeleteConfirm = async () => {
    try {
      await deleteEvent(event.id);
      onDelete(event.id);
      onClose();
    } catch (error) {
      console.error("Failed to delete event", error);
    } finally {
      setIsDeleting(false);
    }
  };
  
  if (isEditing) {
    return (
      <div className="event-form-modal">
        <div className="event-form">
          <h3>Edit Event</h3>
          
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              value={eventData.title}
              onChange={(e) => setEventData({...eventData, title: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={eventData.description || ''}
              onChange={(e) => setEventData({...eventData, description: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Category</label>
            <select 
              value={eventData.category} 
              onChange={(e) => setEventData({...eventData, category: e.target.value})}
            >
              <option value="personal">Personal</option>
              <option value="work">Work</option>
              <option value="family">Family</option>
              <option value="travel">Travel</option>
            </select>
          </div>
          
          <div className="form-actions">
            <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
            <button type="button" onClick={handleSave}>Save Changes</button>
          </div>
        </div>
      </div>
    );
  }
  
  if (isDeleting) {
    return (
      <div className="event-form-modal">
        <div className="event-form">
          <h3>Delete Event</h3>
          <p>Are you sure you want to delete this event?</p>
          <p><strong>{event.title}</strong></p>
          
          <div className="form-actions">
            <button type="button" onClick={() => setIsDeleting(false)}>Cancel</button>
            <button 
              type="button" 
              className="delete-button"
              onClick={handleDeleteConfirm}
            >
              Delete Event
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="event-form-modal">
      <div className="event-form">
        <h3>Event Details</h3>
        
        <div className="event-detail">
          <h4>{event.title}</h4>
          <p className="event-date">
            {format(new Date(event.date), 'MMMM d, yyyy')}
          </p>
          <p className="event-category">
            Category: <span className="category-tag">{event.category}</span>
          </p>
          {event.description && (
            <div className="event-description">
              <p>{event.description}</p>
            </div>
          )}
        </div>
        
        <div className="form-actions">
          <button type="button" onClick={onClose}>Close</button>
          <button type="button" onClick={handleEditClick}>Edit</button>
          <button 
            type="button" 
            className="delete-button"
            onClick={() => setIsDeleting(true)}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}