import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
/*import './styles/index.css'*/
import './styles/resource_HubStyles.css'
/*import Landing_page from './pages/Landing_page.jsx'*/
import Home_page from './pages/Home_page.jsx'
import Footer from './Components/Footer/Footer.jsx'  

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <>
    {/*<Landing_page/>*/}
    <Home_page/>
    </>
  </StrictMode>,
)
