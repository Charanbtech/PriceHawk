import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    trackedProducts: 0,
    unreadNotifications: 0,
    priceDrops: 0,
    totalSavings: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [trackingResponse, notificationsResponse] = await Promise.all([
        axios.get('http://localhost:5000/api/my-products'),
        axios.get('http://localhost:5000/api/my-notifications')
      ]);

      const trackedProducts = trackingResponse.data.products || [];
      const notifications = notificationsResponse.data.notifications || [];
      const unreadCount = notifications.filter(n => !n.is_read).length;

      // Calculate stats
      const priceDrops = trackedProducts.filter(p => 
        p.current_price < p.target_price
      ).length;

      const totalSavings = notifications.reduce((sum, n) => {
        return sum + (n.savings || 0);
      }, 0);

      setStats({
        trackedProducts: trackedProducts.length,
        unreadNotifications: unreadCount,
        priceDrops,
        totalSavings: totalSavings.toFixed(2)
      });

      // Use notifications from previous call
      setRecentActivity((notificationsResponse.data.notifications || []).slice(0, 5));

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-4">
        <h1 style={{fontSize: '2.5rem', fontWeight: '700', color: 'white', marginBottom: '0.5rem'}}>
          📋 Dashboard
        </h1>
        <p style={{color: 'rgba(255,255,255,0.8)', fontSize: '1.125rem'}}>
          Track your savings and monitor price drops
        </p>
      </div>
      
      {/* Stats Cards */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <div className="stat-number">{stats.trackedProducts}</div>
          <div className="stat-label">Tracked Products</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-number">{stats.unreadNotifications}</div>
          <div className="stat-label">New Notifications</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-number">{stats.priceDrops}</div>
          <div className="stat-label">Price Drops</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-number">${stats.totalSavings}</div>
          <div className="stat-label">Total Savings</div>
        </div>
      </div>

      <div className="row">
        {/* Recent Activity */}
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Recent Activity</h3>
            </div>
            <div>
              {recentActivity.length > 0 ? (
                recentActivity.map((activity, index) => (
                  <div key={index} className="notification">
                    <div className="notification-header">
                      <strong>{activity.type?.replace('_', ' ').toUpperCase() || 'PRICE DROP'}</strong>
                      <span className="notification-time">
                        {new Date(activity.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p>{activity.product_name} - Price dropped to ${activity.new_price?.toFixed(2)} (Save ${activity.savings?.toFixed(2)})</p>
                  </div>
                ))
              ) : (
                <p>No recent activity</p>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Quick Actions</h3>
            </div>
            <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
              <a href="/search" className="btn btn-primary">
                🔍 Search Products
              </a>
              <a href="/my-products" className="btn btn-secondary">
                📊 View Tracked Products
              </a>
              <a href="/notifications" className="btn btn-info">
                🔔 Check Notifications
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Welcome Message */}
      {stats.trackedProducts === 0 && (
        <div className="card">
          <div className="card-body text-center" style={{padding: '3rem'}}>
            <div style={{fontSize: '4rem', marginBottom: '1rem'}}>🦅</div>
            <h3 style={{fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem'}}>Welcome to PriceHawk!</h3>
            <p style={{color: '#6b7280', marginBottom: '2rem'}}>Start tracking your favorite products to get notified when prices drop!</p>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem'}}>
              <div style={{padding: '1rem', background: '#f8fafc', borderRadius: '8px'}}>
                <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>🔍</div>
                <div style={{fontWeight: '500'}}>Search Products</div>
              </div>
              <div style={{padding: '1rem', background: '#f8fafc', borderRadius: '8px'}}>
                <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>🎯</div>
                <div style={{fontWeight: '500'}}>Set Target Price</div>
              </div>
              <div style={{padding: '1rem', background: '#f8fafc', borderRadius: '8px'}}>
                <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>🔔</div>
                <div style={{fontWeight: '500'}}>Get Notifications</div>
              </div>
              <div style={{padding: '1rem', background: '#f8fafc', borderRadius: '8px'}}>
                <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>💰</div>
                <div style={{fontWeight: '500'}}>Save Money</div>
              </div>
            </div>
            <a href="/search" className="btn btn-primary" style={{padding: '1rem 2rem', fontSize: '1.125rem'}}>
              🚀 Get Started - Search Products
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;