const NODE_ENV = process.env.NODE_ENV
const production = 'production'

export function isProduction(): boolean {
  return NODE_ENV === production
}

export function isStaging(): boolean {
  const staging = 'staging'
  return process.env.REACT_APP_ENV === staging && !isProduction() 
}
