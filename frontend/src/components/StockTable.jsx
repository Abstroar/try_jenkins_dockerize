import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StockTable = ({ onStockSelect }) => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/stocks');
        // Ensure data is properly formatted
        const formattedStocks = response.data.map(stock => ({
          ...stock,
          current_price: parseFloat(stock.current_price) || 0,
          open_price: parseFloat(stock.open_price) || 0,
          high_price: parseFloat(stock.high_price) || 0,
          low_price: parseFloat(stock.low_price) || 0,
          volume: parseInt(stock.volume) || 0
        }));
        setStocks(formattedStocks);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch stock data');
        setLoading(false);
        console.error('Error fetching stocks:', err);
      }
    };

    fetchStocks();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center p-4">
        {error}
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto rounded-lg">
      <table className="w-full divide-y divide-white/10">
        <thead className="bg-white/5">
          <tr>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              Symbol
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              Current Price
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              Open
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              High
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              Low
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-white/60 uppercase tracking-wider w-1/6">
              Volume
            </th>
          </tr>
        </thead>
        <tbody className="bg-white/5 divide-y divide-white/10">
          {stocks.map((stock) => (
            <tr 
              key={stock.symbol}
              onClick={() => onStockSelect(stock.symbol)}
              className="hover:bg-white/10 transition-colors cursor-pointer"
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white w-1/6">
                {stock.symbol}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-white w-1/6">
                ${stock.current_price?.toFixed(2) || '0.00'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-white w-1/6">
                ${stock.open_price?.toFixed(2) || '0.00'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-white w-1/6">
                ${stock.high_price?.toFixed(2) || '0.00'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-white w-1/6">
                ${stock.low_price?.toFixed(2) || '0.00'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-white w-1/6">
                {stock.volume?.toLocaleString() || '0'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockTable; 