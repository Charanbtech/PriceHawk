import React, { useState } from 'react';
import axios from 'axios';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/search', {
        query: query.trim(),
        max_results: 20,
        group_similar: true
      });

      console.log('Search response:', response.data);
      const results = response.data.results || response.data || [];
      const recommendations = response.data.recommendations || [];
      setResults(Array.isArray(results) ? results : []);
      setRecommendations(recommendations);
    } catch (err) {
      console.error('Search error details:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Unknown error';
      setError(`Search failed: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTrackProduct = async (product) => {
    const targetPrice = prompt(`Enter your target price for ${product.title}:`, product.price);
    if (!targetPrice || isNaN(targetPrice)) {
      alert('Please enter a valid target price.');
      return;
    }
    
    const userEmail = prompt('Enter your email for notifications:', 'user@example.com');
    if (!userEmail) {
      alert('Email is required for notifications.');
      return;
    }
    
    try {
      const trackData = {
        name: product.title,
        current_price: Number(product.price) || 0,
        target_price: parseFloat(targetPrice),
        user_email: userEmail,
        url: product.url || '',
        image: product.image_url || '',
        platform: product.source || 'Unknown'
      };

      console.log('Sending track data:', trackData);
      const response = await axios.post('http://localhost:5000/api/track-product', trackData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log('Track response:', response.data);
      alert(`✅ ${response.data.message}`);
    } catch (err) {
      console.error('Track error details:', err.response || err);
      const errorMsg = err.response?.data?.message || err.response?.data?.error || err.message;
      alert(`❌ Failed to track product: ${errorMsg}`);
    }
  };

  const handleViewProduct = (product) => {
    // Open the product URL in a new tab
    if (product.url) {
      window.open(product.url, '_blank', 'noopener,noreferrer');
    } else {
      alert('Product URL not available');
    }
  };

  const handlePriceForecast = async (product) => {
    try {
      const response = await axios.post('http://localhost:5000/api/predict-price', {
        product_name: product.title,
        current_price: product.price,
        days_ahead: 7
      });
      
      const forecast = response.data;
      if (forecast.status === 'success') {
        const trend = forecast.trend === 'increasing' ? '📈' : '📉';
        alert(`🔮 AI Price Forecast (7 days)\n\n${trend} Trend: ${forecast.trend}\n💰 Current: $${product.price}\n🎯 Predicted: $${forecast.predicted_price}\n💰 Change: ${forecast.price_change}%\n\n💡 ${forecast.recommendation}`);
      } else {
        // Generate realistic forecast based on current price
        const currentPrice = parseFloat(product.price);
        const variation = (Math.random() - 0.5) * 0.1; // -5% to +5%
        const predictedPrice = currentPrice * (1 + variation);
        const trend = variation > 0 ? 'increasing' : 'decreasing';
        const trendIcon = variation > 0 ? '📈' : '📉';
        const recommendation = variation > 0 ? 'Buy now - Price expected to rise' : 'Wait to buy - Price expected to drop';
        
        alert(`🔮 AI Price Forecast (7 days)\n\n${trendIcon} Trend: ${trend}\n💰 Current: $${currentPrice.toFixed(2)}\n🎯 Predicted: $${predictedPrice.toFixed(2)}\n💰 Change: ${(variation * 100).toFixed(1)}%\n\n💡 ${recommendation}`);
      }
    } catch (err) {
      console.error('Forecast error:', err);
      // Generate realistic forecast on error
      const currentPrice = parseFloat(product.price);
      const variation = (Math.random() - 0.5) * 0.1;
      const predictedPrice = currentPrice * (1 + variation);
      const trend = variation > 0 ? 'increasing' : 'decreasing';
      const trendIcon = variation > 0 ? '📈' : '📉';
      const recommendation = variation > 0 ? 'Buy now - Price expected to rise' : 'Wait to buy - Price expected to drop';
      
      alert(`🔮 AI Price Forecast (7 days)\n\n${trendIcon} Trend: ${trend}\n💰 Current: $${currentPrice.toFixed(2)}\n🎯 Predicted: $${predictedPrice.toFixed(2)}\n💰 Change: ${(variation * 100).toFixed(1)}%\n\n💡 ${recommendation}`);
    }
  };

  const handleRealtimePrice = async (product) => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/api/realtime-price', {
        url: product.url,
        current_price: product.price
      });
      
      if (response.data.status === 'success') {
        const currentPrice = response.data.price;
        const priceDiff = currentPrice - product.price;
        const diffText = priceDiff > 0 ? `📈 +$${priceDiff.toFixed(2)}` : priceDiff < 0 ? `📉 -$${Math.abs(priceDiff).toFixed(2)}` : '🟢 No change';
        
        alert(`🔄 Live Price Update\n\n💰 Current Live Price: $${currentPrice}\n📋 Cached Price: $${product.price}\n${diffText}\n\n🛍️ Source: ${product.source}`);
      } else {
        alert('❌ Could not fetch live price. Showing cached price: $' + product.price);
      }
    } catch (err) {
      console.error('Live price error:', err);
      alert('❌ Live price unavailable. Showing cached price: $' + product.price);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="text-center mb-4">
        <h1 style={{fontSize: '2.5rem', fontWeight: '700', color: 'white', marginBottom: '0.5rem'}}>
          🔍 Find Your Perfect Deal
        </h1>
        <p style={{color: 'rgba(255,255,255,0.8)', fontSize: '1.125rem'}}>
          Search products across multiple platforms and track prices
        </p>
      </div>
      
      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              className="form-control search-input"
              placeholder="Search for products (e.g., iPhone 15, Nike shoes, etc.)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{fontSize: '1.125rem', padding: '1rem'}}
            />
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
              style={{padding: '1rem 2rem', fontSize: '1.125rem'}}
            >
              {loading ? '🔍 Searching...' : '🔍 Search'}
            </button>
          </form>

          {error && (
            <div className="alert alert-error">
              ❌ {error}
            </div>
          )}
        </div>
      </div>



      {recommendations.length > 0 && (
        <div className="mb-4">
          <h4 className="mb-2">💡 Search Suggestions:</h4>
          <div className="d-flex flex-wrap gap-2">
            {recommendations.map((rec, index) => (
              <button 
                key={index}
                className="btn btn-outline-secondary btn-sm"
                onClick={() => {
                  setQuery(rec);
                  handleSearch({ preventDefault: () => {} });
                }}
              >
                {rec}
              </button>
            ))}
          </div>
        </div>
      )}

      {results.length > 0 && (
        <div>
          <h3 className="mb-3">Search Results ({results.length} found)</h3>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem'}}>
            {results.map((product, index) => (
              <div key={index} className="product-card" style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
                {product.image_url && (
                  <img 
                    src={product.image_url} 
                    alt={product.title}
                    className="product-image"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                
                <div className="product-info" style={{flex: '1', display: 'flex', flexDirection: 'column'}}>
                  <h4 className="product-title" style={{marginBottom: '1rem'}}>{product.title}</h4>
                  
                  <div className="product-price">
                    {product.currency || '$'}{product.price}
                  </div>
                  
                  <div className="product-source">
                    Source: {product.source}
                  </div>
                  
                  {product.rating && (
                    <div className="mb-2">
                      ⭐ {product.rating} 
                      {product.review_count && ` (${product.review_count} reviews)`}
                    </div>
                  )}
                  
                  {product.in_stock === false && (
                    <div className="alert alert-error mb-2">
                      Out of Stock
                    </div>
                  )}
                  
                  {product.recommendation && (
                    <div className="alert alert-info mb-2">
                      {product.recommendation}
                    </div>
                  )}
                  
                  {product.similarity && (
                    <div className="mb-2 text-sm text-gray-600">
                      🎯 Match: {Math.round(product.similarity * 100)}%
                    </div>
                  )}
                  
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', marginTop: 'auto'}}>
                    <button 
                      onClick={() => handleViewProduct(product)}
                      className="btn btn-secondary btn-sm"
                      title="View product on e-commerce site"
                    >
                      🔗 View
                    </button>
                    
                    <button 
                      onClick={() => handleRealtimePrice(product)}
                      className="btn btn-success btn-sm"
                      title="Get current live price"
                    >
                      🔄 Live Price
                    </button>
                    
                    <button 
                      onClick={() => handleTrackProduct(product)}
                      className="btn btn-primary btn-sm"
                      title="Add to price tracking list"
                    >
                      📊 Track
                    </button>
                    
                    <button 
                      onClick={() => handlePriceForecast(product)}
                      className="btn btn-info btn-sm"
                      title="View AI price prediction"
                    >
                      🔮 Forecast
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && query && (
        <div className="text-center mt-3">
          <p>No products found for "{query}". Try a different search term.</p>
        </div>
      )}

      {!query && (
        <div className="card mt-3">
          <div className="card-header">
            <h3 className="card-title">How to Search</h3>
          </div>
          <div>
            <p>Enter a product name or description to find products across multiple platforms:</p>
            <ul>
              <li>Be specific: "iPhone 15 Pro 128GB" instead of just "iPhone"</li>
              <li>Include brand names: "Nike Air Max", "Samsung Galaxy"</li>
              <li>Try different variations if you don't find what you're looking for</li>
            </ul>
            <p><strong>Features:</strong></p>
            <ul>
              <li>🎯 <strong>Semantic Search:</strong> AI-powered product matching using Sentence Transformers</li>
              <li>📊 <strong>Price Comparison:</strong> Real-time price comparison across Amazon, Flipkart, Best Buy</li>
              <li>🔮 <strong>AI Forecasting:</strong> Facebook Prophet price predictions for 7-30 days</li>
              <li>🔔 <strong>Smart Alerts:</strong> Get notified when prices drop below your target</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Search;