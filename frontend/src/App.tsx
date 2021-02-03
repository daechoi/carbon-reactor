import React from 'react'
import './App.css'
import ApplicationSetup from './features/ApplicationSetup'
import FormTest from './components/formtest'

function App() {
  const onNewColor = (title: string, color: string) => {
    console.log(`title ${title} and color: ${color}`)
  }
  return (
    <div className="App">
      <ApplicationSetup>
        <h2>This is the prop to be sent</h2>
        <FormTest onNewColor={onNewColor} />
      </ApplicationSetup>
    </div>
  )
}

export default App
