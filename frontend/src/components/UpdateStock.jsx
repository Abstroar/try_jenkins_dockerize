import { useState } from 'react';
import { updateStock } from '../api/stockapi';

export function UpdateStock() {
  const [formData, setFormData] = useState({
    symbol: '',
    value: '',
    timestamp: new Date().toISOString()
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    
    try {
      const result = await updateStock(formData);
      setMessage(`Success! Stock updated with ID: ${result.id}`);
      // Reset form
      setFormData({
        symbol: '',
        value: '',
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      setMessage('Failed to update stock. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="stock-form">
      <h2>Update Stock Price</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="symbol">Stock Symbol:</label>
          <input
            id="symbol"
            type="text"
            name="symbol"
            value={formData.symbol}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="value">Price Value:</label>
          <input
            id="value"
            type="number"
            name="value"
            step="0.01"
            value={formData.value}
            onChange={handleChange}
            required
          />
        </div>
        
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Updating...' : 'Update Stock'}
        </button>
      </form>
      
      {message && <p className={message.includes('Success') ? 'success' : 'error'}>{message}</p>}
    </div>
  );
}