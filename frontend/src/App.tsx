import React from 'react'
import './App.css'
import ApplicationSetup from './features/ApplicationSetup'

function App() {
  return (
    <div className="App">
      <ApplicationSetup>
        <h2>This is the prop to be sent</h2>
      </ApplicationSetup>
    </div>
  )
}

export default App
