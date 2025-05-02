// Search.jsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./search.css";

function Search({ setSuggestions }) {
  const [query, setQuery] = useState(""); // Track search input
  const [isLoading, setIsLoading] = useState(false); // To track loading state

  // Function to handle input change
  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  // Fetch suggestions from backend as the user types
  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]); // Avoid search if query is too short
      return;
    }

    const fetchSuggestions = async () => {
      setIsLoading(true); // Set loading state
      try {
        // Make request to the FastAPI search endpoint
        const response = await axios.get(`http://127.0.0.1:8000/search?q=${query}`);
        setSuggestions([response.data]); // Update suggestions with stock data
      } catch (error) {
        console.error("Error fetching stock suggestions", error);
      } finally {
        setIsLoading(false); // Stop loading
      }
    };

    fetchSuggestions(); // Fetch suggestions on input change
  }, [query, setSuggestions]); // Only trigger effect when query changes

  return (
    <div className="search-container">
      <div className="search-input-container">
        <input
          className="search-input"
          type="text"
          placeholder="Search for stocks..."
          value={query}
          onChange={handleInputChange}
        />
      </div>
      
      {/* Show loading spinner when fetching results */}
      {isLoading && (
        <div className="loading-spinner">
          Loading...
        </div>
      )}
    </div>
  );
}

export default Search;
