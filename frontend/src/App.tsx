import { Route, Routes } from 'react-router'
import Footer from './components/Footer'
import Header from './components/Header'
import HomePage from './pages/HomePage/HomePage'

function App() {
  return <>
    <Header></Header>
    <Routes>
      <Route path='/' element={<HomePage></HomePage>}></Route>
    </Routes>
    <Footer></Footer>
  </>
}

export default App
