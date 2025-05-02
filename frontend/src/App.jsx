import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Home from './Home'
import { UpdateStock } from './components/UpdateStock';
import { StockInfo } from './components/StockInfo';

import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import Search from './search'
import IntroPage from './Intropage'
// import Portfolio from './Portfolio';
// import StockData from './StocksData'
import Navbar from './components/Navbar'; 
import StockDisplay from './StockDisplay';
import StockData from './components/graph';
import StockGraph from './components/graph';
import HeroSection from './components/HeroSection';
import StockDashboard from './components/StockDashboard';
import InsightsDashboard from './components/Insights';
import { AuthProvider } from './context/AuthContext';
import Signup from './components/Auth/Signup';
import ProfilePage from './components/Profile/ProfilePage';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  const [startDate, setStartDate] = useState('2021-04-01');
  const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);
  const [aggregate, setAggregate] = useState('monthly');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-neutral-900 text-white relative">
          {/* Glass animated background grid */}
          <div className="fixed inset-0 bg-[radial-gradient(#00ffff10_1px,transparent_1px)] bg-[size:40px_40px] animate-pan z-0" />

          <div className="relative z-10">
            <Navbar isLoggedIn={isLoggedIn} onLogout={() => setIsLoggedIn(false)} />
            
            <main className="container mx-auto px-4 py-8 mt-16">
              <Routes>
                <Route path="/" element={
                  <div className="space-y-8">
                    <HeroSection />
                    <div className="w-full">
                      <StockDashboard />
                    </div>
                  </div>
                } />
                <Route path="/dashboard" element={
                  <div className="space-y-8">
                    <StockDashboard />
                  </div>
                } />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route
                  path="/profile"
                  element={
                    <PrivateRoute>
                      <ProfilePage />
                    </PrivateRoute>
                  }
                />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;


//     <StockData
//       startDate={startDate}
//       endDate={endDate}
//       aggregate={aggregate}
//     />
//   </div>
//     // <Router>
//     //   <div>
//     //     {/* Navbar always visible */}
//     //     <Navbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />

//     //     {/* Define your routes here */}
//     //     <Routes>
//     //       <Route path="/" element={<IntroPage />} />
//     //       <Route path="/register" element={<Register />} />
//     //       <Route path="/login" element={<Login />} />
//     //       <Route path="/display" element={<StockDisplay />} />
//     //       {/* Add Portfolio, StockData, etc. routes later */}
//     //     </Routes>
//     //   </div>
//     // </Router>
//   );
// }

// export default App;
