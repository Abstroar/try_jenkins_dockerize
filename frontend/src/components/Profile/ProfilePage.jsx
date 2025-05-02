import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import axios from 'axios';
import StockDashboard from '../StockDashboard';

const ProfilePage = () => {
  const { user, logout } = useAuth();
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/portfolio', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setPortfolio(response.data);
        if (response.data.symbols.length > 0) {
          setSelectedStock(response.data.symbols[0]);
        }
      } catch (err) {
        setError('Failed to fetch portfolio');
        console.error('Error fetching portfolio:', err);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchPortfolio();
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-white text-center">
          <h2 className="text-2xl mb-4">Please log in to view your profile</h2>
          <a href="/login" className="text-blue-500 hover:text-blue-400">
            Go to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Profile Header */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 mb-8">
          <div className="flex items-center space-x-6">
            <div className="w-24 h-24 rounded-full bg-blue-500 flex items-center justify-center">
              {user.profile_image ? (
                <img
                  src={user.profile_image}
                  alt={user.name}
                  className="w-full h-full rounded-full object-cover"
                />
              ) : (
                <span className="text-4xl text-white">
                  {user.name.charAt(0).toUpperCase()}
                </span>
              )}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">{user.name}</h1>
              <p className="text-gray-400">{user.email}</p>
              <button
                onClick={handleLogout}
                className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Portfolio Section */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
          <h2 className="text-2xl font-bold text-white mb-6">Your Portfolio</h2>
          
          {loading ? (
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
            </div>
          ) : error ? (
            <div className="text-red-500 text-center">
              {error}
            </div>
          ) : (
            <div className="space-y-6">
              {/* Stock Selection */}
              <div className="flex flex-wrap gap-2">
                {portfolio?.symbols.map((symbol) => (
                  <button
                    key={symbol}
                    onClick={() => setSelectedStock(symbol)}
                    className={`px-4 py-2 rounded ${
                      selectedStock === symbol
                        ? 'bg-blue-500 text-white'
                        : 'bg-white/5 text-white hover:bg-white/10'
                    }`}
                  >
                    {symbol}
                  </button>
                ))}
              </div>

              {/* Stock Dashboard */}
              {selectedStock && (
                <StockDashboard selectedStock={selectedStock} />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage; 