import { useEffect, useState } from 'react'
//import Cookies from 'js-cookie'

type IProps = {
  children: React.ReactNode
}

type ICsrfState = {
  csrftoken: string | undefined
  hasError: boolean
  shouldBatch?: boolean
}

const API_KEY = 'GI5P6HGG1PP7DX0S'

const URL = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=BB&interval=1min&apikey=${API_KEY}`

const getCsrfToken = () =>
  //  fetch(process.env.REACT_APP_CSRF_URL || 'http://localhost:8001/csrf', {
  //    mode: 'cors',
  //    credentials: 'include',
  //  })
  new Promise<ICsrfState>((resolve) =>
    setTimeout(() => resolve({ csrftoken: 'wasabi', hasError: false }), 2000)
  ) // two seconds

const ApplicationSetup = ({ ...props }: IProps) => {
  const [csrfToken, setCsrfToken] = useState<ICsrfState | undefined>(undefined)

  // similar to componentdidMount/componentDidUpdate
  useEffect(() => {
    getCsrfToken().then((result) => setCsrfToken(result))
  })

  return (
    <>
      {csrfToken && !csrfToken?.hasError ? (
        <>
          <p> {csrfToken.csrftoken} </p> {props.children}{' '}
        </>
      ) : (
        <h1> Not initialized </h1>
      )}
      fetching from: {URL}
    </>
  )
}

export default ApplicationSetup
