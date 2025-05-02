import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserProfile(token);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserProfile = async (token) => {
    try {
      const response = await axios.get('http://localhost:8000/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
    } catch (err) {
      console.error('Error fetching user profile:', err);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await axios.post('http://localhost:8000/token', formData);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      await fetchUserProfile(access_token);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  const register = async (name, email, password) => {
    try {
      const defaultProfileImage = 'https://www.kindpng.com/picc/m/722-7221920_placeholder-profile-image-placeholder-png-transparent-png.png';
      
      const response = await axios.post('http://localhost:8000/register', {
        name,
        email,
        password,
        profile_image: defaultProfileImage
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      await fetchUserProfile(access_token);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updatePortfolio = async (symbols) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:8000/portfolio', symbols, {
        headers: { Authorization: `Bearer ${token}` }
      });
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update portfolio');
      return false;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updatePortfolio
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}; 