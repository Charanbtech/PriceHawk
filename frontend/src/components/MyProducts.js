import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MyProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      console.log('Fetching products from API...');
      const response = await axios.get('http://localhost:5000/api/my-products');
      console.log('API Response:', response.data);
      setProducts(response.data.products || []);
      setError('');
    } catch (err) {
      console.error('Fetch products error:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Failed to load tracked products';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };



  if (loading) {
    return <div className="text-center mt-4">🔄 Loading your tracked products...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <div>
      <div className="text-center mb-4">
        <h1 style={{fontSize: '2.5rem', fontWeight: '700', color: 'white', marginBottom: '0.5rem'}}>
          📊 My Tracked Products
        </h1>
        <p style={{color: 'rgba(255,255,255,0.8)', fontSize: '1.125rem'}}>
          Monitor your favorite products and track savings
        </p>
      </div>

      {products.length === 0 ? (
        <div className="card">
          <div className="card-body text-center" style={{padding: '3rem'}}>
            <div style={{fontSize: '4rem', marginBottom: '1rem'}}>📊</div>
            <h3 style={{fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem'}}>No products tracked yet</h3>
            <p style={{color: '#6b7280', marginBottom: '2rem'}}>Start tracking products from the search page to see them here.</p>
            <a href="/search" className="btn btn-primary" style={{padding: '1rem 2rem'}}>
              🔍 Search Products
            </a>
          </div>
        </div>
      ) : (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem'}}>
          {products.map((product) => {
            const priceStatus = product.current_price <= product.target_price ? 'success' : 'warning';
            const statusIcon = product.current_price <= product.target_price ? '✅' : '⏳';
            const savings = product.current_price <= product.target_price ? 
              (product.target_price - product.current_price).toFixed(2) : 0;

            return (
              <div key={product._id}>
                <div className="card" style={{height: '100%', display: 'flex', flexDirection: 'column'}}>
                  {product.image_url && (
                    <img 
                      src={product.image_url} 
                      alt={product.product_name}
                      className="card-img-top"
                      style={{ height: '200px', objectFit: 'cover' }}
                      onError={(e) => e.target.style.display = 'none'}
                    />
                  )}
                  
                  <div className="card-body" style={{flex: '1', display: 'flex', flexDirection: 'column'}}>
                    <h5 className="card-title" style={{marginBottom: '1rem'}}>{product.product_name}</h5>
                    
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '1rem'}}>
                      <div>
                        <div style={{fontSize: '0.875rem', color: '#6b7280'}}>Current Price</div>
                        <div style={{fontSize: '1.25rem', fontWeight: '600', color: '#059669'}}>${product.current_price.toFixed(2)}</div>
                      </div>
                      <div style={{textAlign: 'right'}}>
                        <div style={{fontSize: '0.875rem', color: '#6b7280'}}>Target Price</div>
                        <div style={{fontSize: '1.25rem', fontWeight: '600', color: '#4f46e5'}}>${product.target_price.toFixed(2)}</div>
                      </div>
                    </div>
                    
                    <div className={`alert alert-${priceStatus} mb-2`}>
                      {statusIcon} {product.current_price <= product.target_price ? 
                        `Target reached! Save $${savings}` : 
                        `$${(product.current_price - product.target_price).toFixed(2)} above target`
                      }
                    </div>
                    
                    <div className="mb-2">
                      <small className="text-muted">
                        Platform: {product.platform} | 
                        Notifications: {product.notifications_sent || 0}
                      </small>
                    </div>
                    
                    <div className="mb-2">
                      <small className="text-muted">
                        Tracking since: {new Date(product.created_at).toLocaleDateString()}
                      </small>
                    </div>
                  </div>
                  
                  <div className="card-footer" style={{marginTop: 'auto', padding: '1rem', background: '#f8fafc', borderTop: '1px solid #e2e8f0'}}>
                    <div style={{display: 'grid', gridTemplateColumns: product.product_url ? 'repeat(2, 1fr)' : '1fr', gap: '0.5rem'}}>
                      {product.product_url && (
                        <button 
                          onClick={() => window.open(product.product_url, '_blank')}
                          className="btn btn-outline-primary btn-sm"
                        >
                          🔗 View
                        </button>
                      )}
                      <button 
                        onClick={() => alert('📧 Email: ' + product.user_email)}
                        className="btn btn-outline-info btn-sm"
                      >
                        📧 Email
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MyProducts;