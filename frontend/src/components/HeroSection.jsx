import React from "react";
import logo from "../assets/Stock.png";

const HeroSection = () => {
  return (
    <section className="flex flex-col md:flex-row items-center justify-between p-8 gap-8 bg-white/10 backdrop-blur-md rounded-xl shadow-md mb-6">
      {/* Left Content */}
      <div className="max-w-xl">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
          Real-Time Risk Management & Market Trends Analysis
        </h1>
        <p className="text-white/80 mb-6">
          AI-driven insights for better decision-making in the Indian stock market. Get real-time
          analysis and predictions to optimize your investment strategy.
        </p>
        <button className="bg-blue-600 hover:bg-blue-700 transition text-white px-6 py-2 rounded-md font-medium">
          Get Insights Now
        </button>
      </div>

      {/* Right Image */}
      <div className="flex-shrink-0">
        <img
          src={logo}
          alt="Market Graph"
          className="w-72 h-auto rounded-lg shadow"
        />
      </div>
    </section>
  );
};

export default HeroSection; 