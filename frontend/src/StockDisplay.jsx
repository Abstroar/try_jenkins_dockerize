import { useLocation } from 'react-router-dom';

function StockDisplay() {
  const location = useLocation();
  const stockData = location.state?.stockData;

  if (!stockData) {
    return <p>No stock data available.</p>;
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <h2>Stock Details for {stockData.symbol}</h2>
      <ul style={{ listStyle: 'none' }}>
        <li>Current Price: ${stockData.current_price}</li>
        <li>Open Price: ${stockData.open_price}</li>
        <li>High Price: ${stockData.high_price}</li>
        <li>Low Price: ${stockData.low_price}</li>
        <li>Volume: {stockData.volume}</li>
        <li>Date: {stockData.date}</li>
      </ul>
    </div>
  );
}

export default StockDisplay;
