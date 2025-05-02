// frontend/src/graph.jsx
import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import axios from 'axios';

const StockGraph = ({ symbol = 'AMZN' }) => {
  const [stockData, setStockData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTimeRange, setSelectedTimeRange] = useState('1Y');
  const [dateRange, setDateRange] = useState({
    start: "2024-05-01",
    end: "2025-05-01"
  });
  const [aggregation, setAggregation] = useState('monthly');

  const fetchStockData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:8000/stocks-graph`, {
        params: {
          start_date: dateRange.start,
          symbol:symbol,
          end_date: dateRange.end,  
          aggregate: aggregation
        }
      });
      console.log('API Response:', response.data)
      await setStockData(response.data);
    } catch (err) {
      console.error('Error fetching stock data:', err);
      setError(err.response?.data?.detail || 'Failed to fetch stock data');
    } finally {
      setLoading(false);
    }
    
  };
  useEffect(() => {
    console.log('Updated stockData:', stockData);
  }, [stockData]);

  useEffect(() => {
    fetchStockData();
  }, [symbol, dateRange, aggregation]);

  const handleTimeRangeClick = (range) => {
    const end = new Date();
    let start = new Date(end);
    
    switch (range) {
      case '1M':
        start.setMonth(start.getMonth() - 1);
        break;
      case '3M':
        start.setMonth(start.getMonth() - 3);
        break;
      case '6M':
        start.setMonth(start.getMonth() - 6);
        break;
      case '1Y':
        start.setFullYear(start.getFullYear() - 1);
        break;
      case 'ALL':
        start = new Date('2020-01-01');
        break;
      default:
        start = new Date(end.getTime() - 365 * 24 * 60 * 60 * 1000);
    }
    
    setSelectedTimeRange(range);
    setDateRange({
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0]
    });
  };

  if (loading) {
    return (
      <div className="flex flex-col h-full">
        <h2 className="text-lg md:text-xl font-semibold text-white mb-4">
          {symbol} - Stock Price Over Time
        </h2>
        <div className="flex-1 bg-white/5 rounded-lg p-4">
          <div className="h-[400px] flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
              <p className="text-white/80">Loading stock data...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col h-full">
        <h2 className="text-lg md:text-xl font-semibold text-white mb-4">
          {symbol} - Stock Price Over Time
        </h2>
        <div className="flex-1 bg-white/5 rounded-lg p-4">
          <div className="h-[400px] flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
              <div className="text-red-500">{error}</div>
              <button
                onClick={fetchStockData}
                className="px-4 py-2 bg-white/10 text-white/90 rounded-md hover:bg-white/20 transition-colors flex items-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                </svg>
                Reload Data
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!stockData || stockData.length === 0) {
    return (
      <div className="flex flex-col h-full">
        <h2 className="text-lg md:text-xl font-semibold text-white mb-4">
          {symbol} - Stock Price Over Time
        </h2>
        <div className="flex-1 bg-white/5 rounded-lg p-4">
          <div className="h-[400px] flex items-center justify-center">
            <div className="text-yellow-500">No data available for the selected period</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-transparent backdrop-blur-md backdrop-saturate-150 border border-white/20 p-6 rounded-xl shadow-md flex-1">
      <div className="flex flex-col h-full">
        <h2 className="text-lg md:text-xl font-semibold text-white mb-4">
          {symbol} - Stock Price Over Time
        </h2>
        <div className="flex-1 bg-white/5 rounded-lg p-4">
        <ResponsiveContainer width="100%" height={400}>
  <LineChart data={stockData}>
    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
    <XAxis 
      dataKey="date" 
      stroke="#ffffff80"
      tickFormatter={(date) => new Date(date).toLocaleDateString()}
    />
    <YAxis 
      stroke="#ffffff80"
      tickFormatter={(value) => `$${value.toFixed(2)}`}
    />
    <Tooltip 
      formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
      labelFormatter={(date) => new Date(date).toLocaleDateString()}
    />
    <Line 
      type="monotone" 
      dataKey="avg_close" 
      stroke="#00ffff" 
      strokeWidth={2} 
      dot={false}
      activeDot={{ r: 4 }}
    />
  </LineChart>
</ResponsiveContainer>
        </div>

        {/* Controls Section */}
        <div className="mt-4 space-y-4">
          {/* Time Range Buttons */}
          <div className="flex flex-wrap items-center gap-3 py-2">
            <div className="w-24">
              <span className="text-white text-sm font-semibold tracking-wide">Time Range</span>
            </div>
            <div className="flex-1 flex flex-wrap gap-3 justify-start">
              {['1M', '3M', '6M', '1Y', 'ALL'].map((range) => (
              <button
                  key={range}
                  onClick={() => handleTimeRangeClick(range)}
                className={`px-4 py-2.5 rounded-md text-sm font-medium transition-all ${
                    selectedTimeRange === range
                    ? 'bg-blue-600 text-white shadow-lg ring-2 ring-blue-400' 
                    : 'bg-white/10 text-white/90 hover:bg-white/20'
                }`}
              >
                  {range}
              </button>
              ))}
            </div>
          </div>

          {/* Aggregation Buttons */}
          <div className="flex flex-wrap items-center gap-3 py-2">
            <div className="w-24">
              <span className="text-white text-sm font-semibold tracking-wide">Aggregation</span>
            </div>
            <div className="flex-1 flex flex-wrap gap-3 justify-start">
              {['daily', 'weekly', 'monthly', 'yearly'].map((agg) => (
              <button
                  key={agg}
                  onClick={() => setAggregation(agg)}
                className={`px-4 py-2.5 rounded-md text-sm font-medium transition-all ${
                    aggregation === agg
                    ? 'bg-blue-600 text-white shadow-lg ring-2 ring-blue-400' 
                    : 'bg-white/10 text-white/90 hover:bg-white/20'
                }`}
              >
                  {agg.charAt(0).toUpperCase() + agg.slice(1)}
              </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockGraph;