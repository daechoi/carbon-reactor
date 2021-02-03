import { useRef } from 'react'

interface Props {
  onNewColor: (title: string, color: string) => void
}

const FormTest: React.FC<Props> = ({ onNewColor }) => {
  const txtTitle = useRef<HTMLInputElement>(null)
  const hexColor = useRef<HTMLInputElement>(null)

  const submit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const title = txtTitle.current ? txtTitle.current.value : ''
    const color = hexColor.current ? hexColor.current.value : ''

    onNewColor(title, color)

    if (txtTitle.current !== null) txtTitle.current.value = ''
    if (hexColor.current !== null) hexColor.current.value = ''
  }

  return (
    <form onSubmit={(e) => submit(e)}>
      <input ref={txtTitle} type="text" placeholder="placeHolder..." required />
      <input ref={hexColor} type="color" required />
      <button>ADD</button>
    </form>
  )
}

export default FormTest
