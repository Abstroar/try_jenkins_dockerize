import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Home from './Home'
import { UpdateStock } from './components/UpdateStock';
import { StockInfo } from './components/StockInfo';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app-container">
      <header>
        <h1>Stock Market Dashboard</h1>
      </header>
      
      <main>
        <div className="container">
          <UpdateStock />
          <StockInfo />
        </div>
      </main>
    </div>
  )
}

export default App
