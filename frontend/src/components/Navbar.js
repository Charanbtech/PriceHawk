import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../App';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          🦅 PriceHawk
        </Link>
        
        <ul className="navbar-nav">
          <li><Link to="/search">Search</Link></li>
          <li><Link to="/my-products">My Products</Link></li>
          <li><Link to="/notifications">Notifications</Link></li>
          {user ? (
            <>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/tracking">Tracking</Link></li>
              <li>
                <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Welcome, {user.email}</span>
              </li>
              <li>
                <button onClick={logout} className="btn btn-danger btn-sm">Logout</button>
              </li>
            </>
          ) : (
            <>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;