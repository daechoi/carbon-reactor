import * as Sentry from '@sentry/react'
import { Integrations } from '@sentry/tracing'
import { isDefined, isProduction, isStaging } from '../utils'
import LogRocket from 'logrocket'
import setupLogRocketReact from 'logrocket-react'

export const setupLog = () => {
  const errors: Array<string> = []

  const {
    REACT_APP_SENTRY_PUBLIC_DSN,
    REACT_APP_SENTRY_TRACE_SAMPLE_RATE,
    REACT_APP_NAME,
    REACT_APP_VERSION,
    REACT_APP_LOGROCKET_DSN,
    NODE_ENV,
  } = process.env

  isDefined(errors, 'NODE_ENV', NODE_ENV)
  if (isProduction || isStaging) {

    isDefined(errors, 'REACT_APP_SENTRY_TRACE_SAMPLE_RATE', REACT_APP_SENTRY_TRACE_SAMPLE_RATE)
    isDefined(errors, 'REACT_APP_SENTRY_PUBLIC_DSN', REACT_APP_SENTRY_PUBLIC_DSN)
    isDefined(errors, 'REACT_APP_VERSION', REACT_APP_VERSION)
    isDefined(errors, 'REACT_APP_LOGROCKET_DSN', REACT_APP_LOGROCKET_DSN)

    Sentry.init({
      dsn: REACT_APP_SENTRY_PUBLIC_DSN,
      integrations: [new Integrations.BrowserTracing()],
      release: REACT_APP_NAME + '@' + REACT_APP_VERSION,
      environment: isStaging ? 'staging' : isProduction ? 'production' : 'development',
      tracesSampleRate: parseInt(REACT_APP_SENTRY_TRACE_SAMPLE_RATE || '0'), // recommend adjusting in production
    })

    LogRocket.init(REACT_APP_LOGROCKET_DSN||'')
    setupLogRocketReact(LogRocket)
    LogRocket.getSessionURL((sessionURL) => {
      Sentry.configureScope((scope) => {
        scope.setExtra('sessionURL', sessionURL)
      })
    })
    // This is an example script - don't forget to change it!
    //    LogRocket.identify('daechoi', {
    //      name: 'Dae Morrison',
    //      email: 'jamesmorrison@example.com',
    //
    //      // Add your own custom user variables here, ie:
    //      subscriptionType: 'pro',
    //    })

    // Finish setup for Production or Staging logs
  }

  if (errors.length > 0) {
    const message = `FOUND ERROR(s) ON STARTUP: \n${errors.join('\n')}`
    logMessage(message)
  }
}

export const logMessage = (message: string) => {
  isProduction || isStaging ? Sentry.captureMessage(message) : console.log(message)
}
