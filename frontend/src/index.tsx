import React from 'react'
import { render } from 'react-dom'
import './index.scss'
import App from './components/App'
import reportWebVitals from './reportWebVitals'
import { setupLog } from './utils'
import { Provider } from 'react-redux'
import store from './store'

setupLog()

render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
