import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
/*import './styles/index.css'*/
import './styles/resource_HubStyles.css'
/*import Landing_page from './pages/Landing_page.jsx'*/
import Home_page from './pages/Home_page.jsx'
import Resource_archive from './pages/Resources.jsx'
import Footer from './Components/Footer/Footer.jsx'

/*temporary page switch until a router is implemented*/
function getPage() {
  const path = window.location.pathname.replace(/\/$/, '')
  if (path === '/resources') return <Resource_archive/>
  return <Home_page/>
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <>
    {/*<Landing_page/>*/}
    {getPage()}
    </>
  </StrictMode>,
)
