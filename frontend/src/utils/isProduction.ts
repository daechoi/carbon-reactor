const NODE_ENV = process.env.NODE_ENV
const production = 'production'
const staging = 'staging'

export const isProduction = NODE_ENV === production

export const isStaging  = process.env.REACT_APP_ENV === staging && !isProduction
