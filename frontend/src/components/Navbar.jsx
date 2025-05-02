import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import logo from '../assets/Stock.png';
import './Navbar.css';

const Navbar = ({ isLoggedIn, onLogout }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const symbol = searchQuery.trim().toUpperCase();
      if (location.pathname === '/dashboard') {
        // If already on dashboard, just update the URL
        navigate(`/dashboard?symbol=${symbol}`, { replace: true });
      } else {
        // If not on dashboard, navigate to it
        navigate(`/dashboard?symbol=${symbol}`);
      }
      setSearchQuery('');
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <img src={logo} alt="StockTracker Logo" className="navbar-logo-img" />
          <span className="navbar-logo-text">StockTracker</span>
        </Link>

        <form onSubmit={handleSearch} className="navbar-search">
          <input
            type="text"
            placeholder="Search Stock..."
            className="search-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>

        <div className="navbar-auth">
          {isLoggedIn ? (
            <button onClick={onLogout} className="auth-button logout-button">
              Logout
            </button>
          ) : (
            <>
              <Link to="/login" className="auth-button login-button">
                Login
              </Link>
              <Link to="/register" className="auth-button register-button">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
