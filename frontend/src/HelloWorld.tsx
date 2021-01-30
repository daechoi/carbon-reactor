const HelloWorld = () => {
  const sayHello = () => {
    alert('Hello World!')
  }

  return <button onClick={sayHello}>Click me!</button>
}

export default HelloWorld
