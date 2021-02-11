import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import { Navbar } from './Navbar'
import { Loading } from './loading/Loading'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <div>
        <h1>Domanic</h1>
        <Loading isLoading={false} />
      </div>
    </BrowserRouter>
  )
}

export default App
