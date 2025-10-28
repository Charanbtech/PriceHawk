import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/my-notifications');
      setNotifications(response.data.notifications || []);
    } catch (err) {
      setError('Failed to load notifications');
      console.error('Fetch notifications error:', err);
    } finally {
      setLoading(false);
    }
  };

  const sendTestNotification = async () => {
    const email = prompt('Enter your email address for test notification:', 'user@example.com');
    if (!email) return;
    
    try {
      const response = await axios.post('http://localhost:5000/api/send-test-email', {
        email: email
      });
      alert(`✅ ${response.data.message}`);
    } catch (err) {
      const errorMsg = err.response?.data?.message || 'Failed to send test email';
      alert(`❌ ${errorMsg}`);
      console.error('Test email error:', err);
    }
  };

  if (loading) {
    return <div className="text-center mt-4">🔄 Loading notifications...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <div>
      <div className="text-center mb-4">
        <h1 style={{fontSize: '2.5rem', fontWeight: '700', color: 'white', marginBottom: '0.5rem'}}>
          🔔 Notifications
        </h1>
        <p style={{color: 'rgba(255,255,255,0.8)', fontSize: '1.125rem', marginBottom: '1rem'}}>
          Stay updated with price drops and alerts
        </p>
        <button 
          onClick={sendTestNotification}
          className="btn btn-primary"
          style={{padding: '0.75rem 1.5rem'}}
        >
          📧 Send Test Email
        </button>
      </div>

      {notifications.length === 0 ? (
        <div className="card">
          <div className="card-body text-center" style={{padding: '3rem'}}>
            <div style={{fontSize: '4rem', marginBottom: '1rem'}}>🔔</div>
            <h3 style={{fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem'}}>No notifications yet</h3>
            <p style={{color: '#6b7280', marginBottom: '2rem'}}>You'll receive notifications here when tracked product prices drop.</p>
            <a href="/search" className="btn btn-primary" style={{padding: '1rem 2rem'}}>
              🔍 Start Tracking Products
            </a>
          </div>
        </div>
      ) : (
        <div className="notifications-list">
          {notifications.map((notification) => {
            const isRead = notification.is_read;
            const savings = notification.savings || 0;
            const priceDropPercent = ((notification.old_price - notification.new_price) / notification.old_price * 100).toFixed(1);

            return (
              <div 
                key={notification._id} 
                className="card mb-3"
                style={{
                  border: !isRead ? '2px solid #4f46e5' : '1px solid #e2e8f0',
                  background: !isRead ? 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)' : 'white'
                }}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start">
                    <div className="flex-grow-1">
                      <h5 className="card-title">
                        🎉 Price Drop Alert: {notification.product_name}
                        {!isRead && <span className="badge bg-primary ms-2">New</span>}
                      </h5>
                      
                      <div className="row mb-2">
                        <div className="col-md-3">
                          <strong>Old Price:</strong> ${notification.old_price?.toFixed(2)}
                        </div>
                        <div className="col-md-3">
                          <strong>New Price:</strong> 
                          <span className="text-success"> ${notification.new_price?.toFixed(2)}</span>
                        </div>
                        <div className="col-md-3">
                          <strong>Your Target:</strong> ${notification.target_price?.toFixed(2)}
                        </div>
                        <div className="col-md-3">
                          <strong>You Save:</strong> 
                          <span className="text-success"> ${savings.toFixed(2)}</span>
                        </div>
                      </div>
                      
                      <div className="alert alert-success mb-2">
                        📉 Price dropped by {priceDropPercent}% - 
                        {notification.new_price <= notification.target_price ? 
                          ' Target price reached!' : 
                          ' Getting closer to your target!'
                        }
                      </div>
                      
                      <small className="text-muted">
                        📧 Sent to: {notification.user_email} | 
                        📅 {new Date(notification.created_at).toLocaleString()}
                      </small>
                    </div>
                    
                    <div className="ms-3">
                      <div className="text-center">
                        <div className="h2 mb-0 text-success">💰</div>
                        <small>Save ${savings.toFixed(2)}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="card mt-4">
        <div className="card-header">
          <h5>📧 Email Notification Settings</h5>
        </div>
        <div className="card-body">
          <p>Email notifications are automatically sent when:</p>
          <ul>
            <li>✅ Product price drops below your target price</li>
            <li>📉 Product price drops from the current tracked price</li>
            <li>🎯 Significant price changes are detected</li>
          </ul>
          <p className="text-muted">
            <strong>Note:</strong> Make sure to provide a valid email address when tracking products.
            Check your spam folder if you don't receive notifications.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Notifications;