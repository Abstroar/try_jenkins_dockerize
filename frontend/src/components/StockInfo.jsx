import { useState } from 'react';
import { getStock } from '../api/stockapi';

export function StockInfo() {
  const [symbol, setSymbol] = useState('');
  const [stock, setStock] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbol.trim()) return;
    
    setIsLoading(true);
    setError('');
    setStock(null);
    
    try {
      const result = await getStock(symbol);
      if (result.message === 'Stock not found') {
        setError('Stock not found');
      } else {
        setStock(result);
      }
    } catch (err) {
      setError('Error fetching stock data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="stock-info">
      <h2>Find Stock Information</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="search-symbol">Enter Stock Symbol:</label>
          <input
            id="search-symbol"
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="e.g., AAPL"
            required
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>
      
      {error && <p className="error">{error}</p>}
      
      {stock && (
        <div className="stock-details">
          <h3>{stock.symbol} Details</h3>
          <p><strong>Price:</strong> ${stock.value.toFixed(2)}</p>
          <p><strong>Last Updated:</strong> {new Date(stock.timestamp).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
}