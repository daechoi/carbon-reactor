import { useState } from 'react'
import Cookies from 'js-cookie'

interface ICsrfToken {
  csrftoken: string
}

const ApplicationSetup = (Props, State) => {
  const [csrfToken, setCsrfToken] = useState<ICsrfToken | undefined>(undefined)

  const getCsrfToken = () => {
    fetch(process.env.REACT_APP_CSRF_URL || 'http://localhost:8001/csrf', {
      mode: 'cors',
      credentials: 'include',
    }).then((response) => {
      if (response.ok) {
        setCsrfToken({
          csrftoken: Cookies.get('csrf'),
        })
        return response.json()
      }
    })
  }
  //     mode: 'cors',
  //     credentials: 'include',
  //   }).then((success => {
  //     setCsrfToken({csrftoken: Cookies.get('csrftoken')})
  //   });
  //   return success.json()
  // }, failure => {
  //   console.error('Failed to set CSRF Token', failure);
  //   setCsrfToken({hasError: true, csrftoken: null});
  //   logToSentry(failure);
  //   return { enable_gql_batching: null };
  // }).then( res =>{
  //   const shouldBatch:
  // } )
  //
}
