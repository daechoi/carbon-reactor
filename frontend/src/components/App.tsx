import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import { Navbar } from './Navbar'
import { Loading } from './loading/Loading'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <div>
        <h1>Number my days!</h1>
        <h2>A Scheduling software by hour by subject</h2>
        <p>A thousand miles journey begins with one step</p>
        <p>that begins with a character....that begins with one letter...</p>
        would be awesome to have vim binding so that I can do everything on keyboard without leaving it...at
        the speed of thought. and be able to open anywhere...including from the phone...whatever i was
        thinking or want to contribute.
        <Loading isLoading={false} />
      </div>
    </BrowserRouter>
  )
}

export default App
