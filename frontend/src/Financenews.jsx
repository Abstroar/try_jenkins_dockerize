import React, { useState, useEffect } from 'react';
import './FinancialNews.css'; // We'll create this CSS file next

const FinancialNews = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulating API fetch with mock data
    const fetchNews = async () => {
      try {
        // In a real app, you would fetch from a financial news API
        // const response = await fetch('https://api.example.com/financial-news');
        // const data = await response.json();
        
        // Mock data
        const mockNews = [
          {
            id: 1,
            title: 'Federal Reserve Holds Interest Rates Steady',
            summary: 'The Federal Reserve maintained interest rates at current levels, signaling potential cuts later this year as inflation shows signs of cooling.',
            source: 'Financial Times',
            date: '2023-11-01',
            imageUrl: 'https://example.com/fed-image.jpg'
          },
          {
            id: 2,
            title: 'Tech Stocks Rally After Strong Earnings Reports',
            summary: 'Major tech companies reported better-than-expected earnings, leading to a 3% surge in the NASDAQ composite index.',
            source: 'Wall Street Journal',
            date: '2023-11-02',
            imageUrl: 'https://example.com/tech-stocks.jpg'
          },
          {
            id: 3,
            title: 'Bitcoin Surges Past $35,000 Amid ETF Speculation',
            summary: 'Cryptocurrency markets rallied as investors grew optimistic about the potential approval of a spot Bitcoin ETF in the US.',
            source: 'CoinDesk',
            date: '2023-11-03',
            imageUrl: 'https://example.com/bitcoin-chart.jpg'
          },
          {
            id: 4,
            title: 'Oil Prices Jump After Middle East Tensions Escalate',
            summary: 'Brent crude rose 4% following renewed geopolitical tensions in key oil-producing regions.',
            source: 'Bloomberg',
            date: '2023-11-04',
            imageUrl: 'https://example.com/oil-prices.jpg'
          }
        ];

        setNews(mockNews);
        setLoading(false);
      } catch (err) {
        setError('Failed to load financial news');
        setLoading(false);
        console.error('Error fetching news:', err);
      }
    };

    fetchNews();
  }, []);

  if (loading) {
    return <div className="loading">Loading financial news...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="financial-news-container">
      <h2 className="news-header">Latest Financial News</h2>
      <div className="news-grid">
        {news.map((item) => (
          <div key={item.id} className="news-card">
            {item.imageUrl && (
              <div className="news-image">
                <img src={item.imageUrl} alt={item.title} />
              </div>
            )}
            <div className="news-content">
              <h3 className="news-title">{item.title}</h3>
              <p className="news-summary">{item.summary}</p>
              <div className="news-meta">
                <span className="news-source">{item.source}</span>
                <span className="news-date">{new Date(item.date).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FinancialNews;