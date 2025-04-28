import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);


  const stockSymbols = [
    'AAPL', 'GOOGL',
  ];


  const apiKey = 'd02p359r01qi6jgif6p0d02p359r01qi6jgif6pg';
  const apiUrl = 'https://finnhub.io/api/v1/quote';

  const fetchStockData = async (symbols) => {
    try {
      const stockData = await Promise.all(
        symbols.map(async (symbol) => {
          const response = await axios.get(apiUrl, {
            params: {
              symbol: symbol,
              token: apiKey
            }
          });

          const { c: currentPrice } = response.data;

          return { symbol, value: currentPrice };
        })
      );

      return stockData;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      return [];
    }
  };

  // Function to fetch data for stocks
  const fetchStocksForDay = async () => {
    setLoading(true); // Set loading to true when fetching data
    const stockData = await fetchStockData(stockSymbols);
    setStocks(stockData);
    setLoading(false); // Set loading to false once data is fetched

    // Cache data in localStorage
    localStorage.setItem('stockData', JSON.stringify(stockData));
  };

  useEffect(() => {
    // Check if cached data exists
    const cachedData = localStorage.getItem('stockData');
    if (cachedData) {
      setStocks(JSON.parse(cachedData));
      setLoading(false); // Set loading to false if data is cached
    } else {
      fetchStocksForDay();
    }

    // Optionally refresh the data every 24 hours
    const intervalId = setInterval(() => {
      fetchStocksForDay();
    }, 86400000); // 24 hours in milliseconds

    // Cleanup on component unmount
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return <div>Loading stocks...</div>;
  }

  return (
    <div>
      <h1>Stock Prices</h1>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.symbol}>
            {stock.symbol}: ${stock.value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;
