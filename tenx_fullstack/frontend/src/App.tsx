import { Route, Routes } from 'react-router-dom'
import HomePage from './HomePage'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'

function App() {
  return (
    <>
      <div>
        <Routes>
          <Route path="/wallet" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </div>
    </>
  )
}

export default App
