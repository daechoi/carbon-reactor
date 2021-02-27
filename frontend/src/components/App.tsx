import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import { Navbar } from './Navbar'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        This is a research management application to track internal sentiment, time-line, and alerts.
      </main>
    </BrowserRouter>
  )
}

export default App
