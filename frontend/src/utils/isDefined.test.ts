import isDefined from './isDefined'

describe('isDefined', () => {
  const errors: Array<string> = []
  beforeEach(() => {
    errors.length = 0 // clear array without creating a new array
  })

  test('Populates errors[] if the variable is not defined', () => {
    isDefined(errors, 'VARIABLE', undefined)
    expect(errors[0]).toBe('- ENV VARIABLE was not defined!  This variable is required')
  })

  test('Returns no error if the variable is defined', () => {
    isDefined(errors, 'VARIABLE', 'DEFINED')
    expect(errors.length).toEqual(0)
  })
})
