import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockGraph from './graph';
import { useLocation } from 'react-router-dom';

const StockDetailsPanel = ({ selectedStock }) => {
  const [stockDetails, setStockDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStockDetails = async () => {
    if (!selectedStock) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const symbol = selectedStock.toUpperCase();
      
      // Get current stock data
      const response = await axios.get(`http://localhost:8000/api/fetch-stock/${symbol}`);
      console.log(response.data);
      if (response.data && response.data.current_price) {
        const currentData = response.data;
        setStockDetails({
          currentPrice: parseFloat(currentData.current_price),
          open: parseFloat(currentData.open_price),
          high: parseFloat(currentData.high_price),
          low: parseFloat(currentData.low_price),
          volume: parseInt(currentData.volume),
          date: currentData.date
        });
      } else {
        setError('Failed to fetch stock data');
      }
    } catch (err) {
      console.error('Error fetching stock details:', err);
      if (err.response?.status === 404) {
        setError(`Stock ${selectedStock} not found. Please verify the stock symbol and try again.`);
      } else if (err.response?.status === 429) {
        setError('Rate limit reached. Please wait a moment and try again.');
      } else if (err.response?.status === 500) {
        setError('Server error while fetching stock data. Please try again later.');
      } else {
        setError('Failed to fetch stock data. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStockDetails();
  }, [selectedStock]);

  if (loading) return <div className="text-white">Loading stock data...</div>;
  if (error) return <div className="text-red-500 p-4 bg-red-500/10 rounded-lg">{error}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
      {/* Graph - 50% width */}
      <div className="bg-white/5 rounded-lg p-4 w-full">
        <h3 className="text-lg font-semibold text-white mb-4">Stock Graph</h3>
        <div className="w-full h-[300px]">
        <StockGraph symbol={selectedStock} />
        </div>
      </div>
      
      {/* Details - 50% width */}
      <div className="bg-white/5 rounded-lg p-4 w-full">
        <h3 className="text-lg font-semibold text-white mb-4">Stock Details</h3>
        {stockDetails ? (
          <div className="space-y-2 text-white">
            <p>Current Price: ${stockDetails.currentPrice?.toFixed(2) || 'N/A'}</p>
            <p>Open: ${stockDetails.open?.toFixed(2) || 'N/A'}</p>
            <p>High: ${stockDetails.high?.toFixed(2) || 'N/A'}</p>
            <p>Low: ${stockDetails.low?.toFixed(2) || 'N/A'}</p>
            <p>Volume: {stockDetails.volume ? stockDetails.volume.toLocaleString() : 'N/A'}</p>
            <p>Last Updated: {stockDetails.date ? new Date(stockDetails.date).toLocaleString() : 'N/A'}</p>
          </div>
        ) : (
          <div className="text-gray-400">No data available</div>
        )}
      </div>
    </div>
  );
};

const StockDashboard = () => {
  const location = useLocation();
  const [selectedStock, setSelectedStock] = useState('AMZN');

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const symbol = params.get('symbol');
    if (symbol) {
      setSelectedStock(symbol.toUpperCase());
    }
  }, [location]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-white mb-6">
        {selectedStock} Stock Dashboard
      </h2>
      <StockDetailsPanel selectedStock={selectedStock} />
    </div>
  );
};

export default StockDashboard;
