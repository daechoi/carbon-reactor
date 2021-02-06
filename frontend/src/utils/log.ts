import * as Sentry from '@sentry/react'
import { Integrations } from '@sentry/tracing'
import { isDefined, isProduction, isStaging } from '../utils'

export const setupLog = () => {
  const errors: Array<string> = []

  const {
    REACT_APP_SENTRY_PUBLIC_DSN,
    REACT_APP_SENTRY_TRACE_SAMPLE_RATE,
    REACT_APP_NAME,
    REACT_APP_VERSION,
    NODE_ENV,
  } = process.env

  isDefined(errors, 'NODE_ENV', NODE_ENV)
  isDefined(errors, 'REACT_APP_SENTRY_TRACE_SAMPLE_RATE', REACT_APP_SENTRY_TRACE_SAMPLE_RATE)

  isDefined(errors, 'REACT_APP_SENTRY_PUBLIC_DSN', REACT_APP_SENTRY_PUBLIC_DSN)
  isDefined(errors, 'REACT_APP_VERSION', REACT_APP_VERSION)

  Sentry.init({
    dsn: REACT_APP_SENTRY_PUBLIC_DSN,
    integrations: [new Integrations.BrowserTracing()],
    release: REACT_APP_NAME+'@' + REACT_APP_VERSION,
    environment: isStaging()? 'staging': isProduction()?'production':'development',
    tracesSampleRate: parseInt(REACT_APP_SENTRY_TRACE_SAMPLE_RATE || '0'), // recommend adjusting in production
  })

  if (errors.length > 0) {
    const message = `FOUND ERROR(s) ON STARTUP: \n${errors.join('\n')}`
    isProduction() || isStaging() ? Sentry.captureMessage(message) : console.log(message)
  }
}

export const logMessage = (message: string) => {
  Sentry.captureMessage(message)
}
