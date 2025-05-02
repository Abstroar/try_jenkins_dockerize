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

function StockGraph({ startDate, endDate, aggregate }) {
  const [stockData, setStockData] = useState([]);

  useEffect(() => {
    async function fetchStockData() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/stocks?start_date=${startDate}&end_date=${endDate}&aggregate=${aggregate}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStockData(data);
      } catch (error) {
        console.error('Error fetching stock data:', error);
      }
    }

    fetchStockData();
  }, [startDate, endDate, aggregate]);

  // Hardcoded Apple stock data for today
  const appleTodayData = {
    symbol: 'AAPL',
    date: new Date().toLocaleDateString(),
    open: 193.62,
    high: 194.85,
    low: 192.43,
    close: 193.58,
    volume: '28.3M',
    change: -0.04,
    changePercent: -0.02,
    riskEstimate: 'Medium', // Risk estimation
    riskFactors: [
      'Market volatility',
      'Upcoming earnings report',
      'Sector rotation'
    ]
  };

  // Calculate risk score (example calculation)
  const riskScore = Math.min(Math.floor(Math.random() * 70) + 30, 100); // Random between 30-100

  return (
    <div style={{ display: 'flex', gap: '20px', width: '100%' }}>
      {/* Graph Section - Left Side */}
      <div style={{ flex: 2, height: '500px' }}>
        <h2>Stock Price Over Time</h2>
        <ResponsiveContainer width="100%" height="80%">
          <LineChart
            data={stockData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(date) => new Date(date).toLocaleDateString()} 
            />
            <YAxis 
              domain={['auto', 'auto']} 
              tickFormatter={(value) => `$${value.toFixed(2)}`}
            />
            <Tooltip 
              formatter={(value) => [`$${value.toFixed(2)}`, 'Average Close']}
              labelFormatter={(date) => `Date: ${new Date(date).toLocaleDateString()}`}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="avg_close"
              stroke="#8884d8"
              activeDot={{ r: 8 }}
              name="Average Close Price"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Table Section - Right Side */}
      <div style={{ flex: 1 }}>
        <h2>AAPL - Today's Data</h2>
        <div style={{ 
          background: '#f8f9fa', 
          padding: '20px', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <tbody>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Symbol</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{appleTodayData.symbol}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Date</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{appleTodayData.date}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Open</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>${appleTodayData.open.toFixed(2)}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>High</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>${appleTodayData.high.toFixed(2)}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Low</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>${appleTodayData.low.toFixed(2)}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Close</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>${appleTodayData.close.toFixed(2)}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Volume</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{appleTodayData.volume}</td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Change</td>
                <td style={{ 
                  padding: '8px', 
                  borderBottom: '1px solid #ddd',
                  color: appleTodayData.change >= 0 ? '#28a745' : '#dc3545'
                }}>
                  {appleTodayData.change >= 0 ? '+' : ''}{appleTodayData.change.toFixed(2)} ({appleTodayData.changePercent.toFixed(2)}%)
                </td>
              </tr>
              <tr>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>Risk Estimate</td>
                <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div style={{
                      width: '16px',
                      height: '16px',
                      borderRadius: '50%',
                      background: riskScore > 70 ? '#dc3545' : riskScore > 40 ? '#ffc107' : '#28a745',
                      marginRight: '8px'
                    }} />
                    {appleTodayData.riskEstimate} (Score: {riskScore})
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          {/* Risk Factors Section */}
          <div style={{ marginTop: '20px' }}>
            <h4 style={{ marginBottom: '10px' }}>Risk Factors:</h4>
            <ul style={{ paddingLeft: '20px', margin: 0 }}>
              {appleTodayData.riskFactors.map((factor, index) => (
                <li key={index} style={{ marginBottom: '5px' }}>{factor}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StockGraph;