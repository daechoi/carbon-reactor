import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import { Navbar } from './Navbar'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar>
        <div>
          <h1>Domanic</h1>
        </div>
      </Navbar>
    </BrowserRouter>
  )
}

export default App
