const API_BASE_URL = 'http://localhost:8000';

export const updateStock = async (stockData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/update-stock`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(stockData),
    });
    return await response.json();
  } catch (error) {
    console.error('Error updating stock:', error);
    throw error;
  }
};

export const getStock = async (symbol) => {
  try {
    const response = await fetch(`${API_BASE_URL}/get-stock/${symbol}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching stock:', error);
    throw error;
  }
};