import React from "react";
import StockTable from './StockTable';

const InsightsDashboard = () => {
  return (
    <div className="space-y-12 p-6">
      <section className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-md">
        <h2 className="text-xl font-semibold text-white mb-4">Stock List</h2>
        <StockTable onStockSelect={() => {}} />
      </section>

      {/* Predictions + Risk Alerts */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-4 bg-white/10 border border-white/10 backdrop-blur-md rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2 text-white">Market Prediction</h3>
          <div className="h-32 bg-blue-200/30 rounded-md animate-pulse" />
          <p className="mt-2 text-green-400 text-sm">Confidence: 92%</p>
        </div>
        <div className="p-4 bg-white/10 border border-white/10 backdrop-blur-md rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4 text-white">Risk Alerts</h3>
          <ul className="space-y-3 text-sm text-white/90">
            <li className="flex justify-between items-center bg-red-400/10 p-2 rounded-md">
              <div>
                <p className="font-semibold text-red-300">Reliance Industries</p>
                <p className="text-xs">Unusual volume spike detected</p>
              </div>
              <span className="text-xs text-white/60">10 mins ago</span>
            </li>
            <li className="flex justify-between items-center bg-yellow-300/10 p-2 rounded-md">
              <div>
                <p className="font-semibold text-yellow-200">HDFC Bank</p>
                <p className="text-xs">Volatility above average</p>
              </div>
              <span className="text-xs text-white/60">25 mins ago</span>
            </li>
            <li className="flex justify-between items-center bg-green-300/10 p-2 rounded-md">
              <div>
                <p className="font-semibold text-green-200">TCS</p>
                <p className="text-xs">Support level reached</p>
              </div>
              <span className="text-xs text-white/60">45 mins ago</span>
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default InsightsDashboard; 