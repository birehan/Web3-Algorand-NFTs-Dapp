import { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { Route, Routes } from 'react-router-dom'
import HomePage from './HomePage'
import { setUpAxiosIntercept } from './api/request'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'

function App() {
  const { user } = useSelector((state: any) => state.auth)
  useEffect(() => {
    if (user) {
      setUpAxiosIntercept(user)
    }
    return () => {}
  }, [user])

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
