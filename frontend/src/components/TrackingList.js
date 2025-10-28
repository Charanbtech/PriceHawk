import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TrackingList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTrackedProducts();
  }, []);

  const fetchTrackedProducts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/my-products');
      setProducts(response.data.products || []);
    } catch (err) {
      setError('Failed to load tracked products');
      console.error('Error fetching tracked products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUntrack = async (productId) => {
    if (!window.confirm('Are you sure you want to stop tracking this product?')) {
      return;
    }

    try {
      await axios.delete(`http://localhost:5000/api/untrack-product/${productId}`);
      setProducts(products.filter(p => p._id !== productId));
      alert('Product untracked successfully!');
    } catch (err) {
      alert('Failed to untrack product');
      console.error('Error untracking product:', err);
    }
  };

  const handleUpdateTargetPrice = async (productId, newTargetPrice) => {
    try {
      await axios.patch(`http://localhost:5000/api/update-target-price/${productId}`, {
        target_price: parseFloat(newTargetPrice)
      });
      
      // Update local state
      setProducts(products.map(p => 
        p._id === productId 
          ? { ...p, target_price: parseFloat(newTargetPrice) }
          : p
      ));
      alert('Target price updated!');
    } catch (err) {
      alert('Failed to update target price');
      console.error('Error updating target price:', err);
    }
  };

  const getPriceStatus = (product) => {
    if (!product.target_price) return null;
    
    if (product.current_price <= product.target_price) {
      const savings = product.target_price - product.current_price;
      return { status: 'success', message: `Target reached! Save $${savings.toFixed(2)}` };
    } else {
      const diff = product.current_price - product.target_price;
      return { 
        status: 'warning', 
        message: `$${diff.toFixed(2)} above target` 
      };
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading tracked products...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="mb-3">My Tracked Products ({products.length})</h1>
      
      {products.length === 0 ? (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">No Products Tracked Yet</h3>
          </div>
          <div>
            <p>You haven't started tracking any products yet.</p>
            <a href="/search" className="btn btn-primary">
              Search Products to Track
            </a>
          </div>
        </div>
      ) : (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '1.5rem'}}>
          {products.map((product) => {
            const priceStatus = getPriceStatus(product);
            const savings = product.original_price > product.current_price 
              ? product.original_price - product.current_price 
              : 0;

            return (
              <div key={product._id} className="product-card" style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
                {product.image_url && (
                  <img 
                    src={product.image_url} 
                    alt={product.name}
                    className="product-image"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                
                <div className="product-info" style={{flex: '1', display: 'flex', flexDirection: 'column', padding: '1.5rem'}}>
                  <h4 className="product-title" style={{marginBottom: '1rem'}}>{product.product_name}</h4>
                  
                  <div className="product-price">
                    Current: ${product.current_price.toFixed(2)}
                    {savings > 0 && (
                      <span className="text-success ml-2">
                        (Save ${savings.toFixed(2)})
                      </span>
                    )}
                  </div>
                  
                  <div className="product-source mb-2">
                    Source: {product.platform} | 
                    Tracking since: {new Date(product.created_at).toLocaleDateString()}
                  </div>

                  <div className="mb-2">
                    Target Price: ${product.target_price.toFixed(2)}
                  </div>

                  {priceStatus && (
                    <div className={`alert alert-${priceStatus.status} mb-2`}>
                      {priceStatus.message}
                    </div>
                  )}
                  
                  <div className="form-group mb-2">
                    <label>Target Price:</label>
                    <div className="d-flex gap-2">
                      <input
                        type="number"
                        step="0.01"
                        className="form-control"
                        value={product.target_price || ''}
                        onChange={(e) => {
                          if (e.target.value) {
                            handleUpdateTargetPrice(product._id, e.target.value);
                          }
                        }}
                        placeholder="Set target price"
                      />
                    </div>
                  </div>
                  
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginTop: 'auto'}}>
                    <a 
                      href={product.product_url || '#'} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="btn btn-secondary btn-sm"
                      onClick={(e) => {
                        if (!product.product_url) {
                          e.preventDefault();
                          alert('Product URL not available');
                        }
                      }}
                    >
                      🔗 View
                    </a>
                    
                    <button 
                      onClick={() => handleUntrack(product._id)}
                      className="btn btn-danger btn-sm"
                    >
                      ❌ Stop
                    </button>
                  </div>
                  
                  <div className="mt-2">
                    <small className="text-muted">
                      Last checked: {new Date(product.created_at).toLocaleString()}
                    </small>
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

export default TrackingList;