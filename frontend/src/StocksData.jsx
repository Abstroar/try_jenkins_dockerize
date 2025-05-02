import { useState, useEffect } from 'react';

function StockData() {
  const [symbol, setSymbol] = useState('');        // State to store user input
  const [stockData, setStockData] = useState(null); // State to store fetched stock data
  const [error, setError] = useState(null);         // State to store error messages

  const fetchStockData = async () => {
    try {
      const response = await fetch(`/stock/${symbol}`); // Send the entered symbol to backend
      if (!response.ok) {
        throw new Error('Stock not found');
      }
      const data = await response.json();
      setStockData(data); // Update state with the fetched data
      setError(null);      // Reset any previous errors
    } catch (error) {
      setError(error.message); // Set error message if fetch fails
      setStockData(null);      // Reset stock data if error occurs
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();  // Prevent page reload on form submit
    if (symbol.trim()) {
      fetchStockData();  // Fetch data if symbol is valid
    }
  };

  return (
    <div>
      <h2>Search for a Stock</h2>
      
      {/* Search bar */}
      <form onSubmit={handleSearchSubmit}>
        <input 
          type="text" 
          value={symbol} 
          onChange={(e) => setSymbol(e.target.value.toUpperCase())} // Capitalize symbol
          placeholder="Enter stock symbol (e.g., AAPL)"
        />
        <button type="submit">Search</button>
      </form>

      {/* Displaying error or loading message */}
      {error && <p>{error}</p>}

      {/* Displaying stock data */}
      {stockData ? (
        <div>
          <h3>Stock Data for {stockData.symbol}</h3>
          <ul>
            <li>Current Price: ${stockData.current_price}</li>
            <li>Open Price: ${stockData.open_price}</li>
            <li>High Price: ${stockData.high_price}</li>
            <li>Low Price: ${stockData.low_price}</li>
            <li>Volume: {stockData.volume}</li>
            <li>Date: {stockData.date}</li>
          </ul>
        </div>
      ) : (
        <p>{symbol ? 'Loading...' : 'Enter a stock symbol to search.'}</p>
      )}
    </div>
  );
}

export default StockData;
