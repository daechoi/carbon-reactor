// not sure if I should carry around the errors like this.  
const isDefined = (errors: Array<string> = [], name: string, e?:string) => {
  if (e === null || typeof e === 'undefined'){
    errors.push(`- ENV ${name} was not defined!  This variable is required`)
  }
}

export default isDefined
