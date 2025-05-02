export async function searchStock(symbol) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/stock/${symbol}`);
    if (!response.ok) {
      throw new Error('Stock not found');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
}