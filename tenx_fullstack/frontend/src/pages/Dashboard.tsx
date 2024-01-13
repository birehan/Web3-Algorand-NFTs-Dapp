import { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import Certificates from '../components/Certificates'
import DesktopSidebar from '../components/DesktopSidebar'
import Header from '../components/Header'
import Sidebar from '../components/Sidebar'

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user } = useSelector((state: any) => state.auth)
  const navigate = useNavigate()

  useEffect(() => {
    if (!user) {
      navigate('/login')
    }

    return () => {}
  }, [user])

  return (
    <>
      <div>
        <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
        <DesktopSidebar />

        <div className="lg:pl-72">
          <Header setSidebarOpen={setSidebarOpen} />
          <main className="py-6 px-6 xl:px-20">
            <Certificates />
            {/* <Suspense fallback={<Loading />}>
              <Outlet />
            </Suspense> */}
          </main>
        </div>
      </div>
    </>
  )
}
