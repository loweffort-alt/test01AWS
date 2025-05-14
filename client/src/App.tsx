import { useState } from 'react'
import { devMode, apiUrl, productionUrl } from '../config.ts'

const fuentes = ["interfase | F-3a", "interfase | F-4a", "interfase | F-5a.1",
  "intraplaca | F-3b", "intraplaca | F-3c", "intraplaca | F-4b",
  "intraplaca | F-4c.1", "intraplaca | F-4c.2", "intraplaca | F-5b.1",
  "intraplaca | F-5c.1",
  "corteza | PSw-3", "corteza | PSw-4", "corteza | PSe-3", "corteza | PSe-5",
  "corteza | PSw-5", "corteza | PSe-4", "corteza | PSe-6"]

let url = ""

function App() {
  const [fuente, setFuente] = useState(fuentes[0])
  const [upper, setUpper] = useState(5)
  const [bottom, setBottom] = useState(80)
  const [preview, setPreview] = useState("")

  if (devMode == "development") {
    url = `${apiUrl}/generate-seismic-fonts`
  } else if (devMode == "production") {
    url = `${productionUrl}/generate-seismic-fonts`
  } else {
    return <div>Error: No config found</div>
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Aquí puedes manejar el envío del formulario
    try {
      const formData = new URLSearchParams()
      formData.append('fuente', fuente)
      formData.append('upper', upper.toString())
      formData.append('bottom', bottom.toString())

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
      })
      const html = await response.json()
      console.log(html)
      setPreview(html.url)
    } catch (error) {
      console.error("Error fetching data:", error)
      setPreview("<p style='color:red'>Error al generar el gráfico</p>")
    }
  }

  return (
    <>
      <div className='w-screen flex h-screen'>
        <div className='w-1/2 border-r border-r-stone-700 flex flex-col justify-center items-center'>
          <form onSubmit={handleSubmit}>
            <div className='flex flex-col'>
              <h2 className="mb-8">Inserta los datos:</h2>
              <label htmlFor="fuente">Fuente</label>
              <select
                name="fuente"
                id="fuente"
                className='border border-stone-700 mb-4 py-1 px-2'
                value={fuente}
                onChange={(e) => setFuente(e.target.value)}
              >
                {fuentes.map((fuente, index) => (
                  <option key={index} value={fuente} className="bg-stone-800">
                    {fuente}
                  </option>
                ))}
              </select>

              <label htmlFor="upper">Upper</label>
              <input
                type="number"
                name="upper"
                id="upper"
                className='border border-stone-700 mb-4 py-1 px-2'
                value={upper}
                onChange={(e) => setUpper(Number(e.target.value))}
              />

              <label htmlFor="bottom">Bottom</label>
              <input
                type="number"
                name="bottom"
                id="bottom"
                className='border border-stone-700 mb-4 py-1 px-2'
                value={bottom}
                onChange={(e) => setBottom(Number(e.target.value))}
              />

              <button
                type="submit"
                className='bg-stone-700 text-white p-2 rounded-md'
              >
                Submit
              </button>
            </div>
          </form>
        </div>
        <div className="w-1/2  border-l border-l-stone-700 flex flex-col justify-center items-center">
          {preview ? (
            <iframe
              src={preview}
              className="w-full h-full"
              style={{ border: 'none' }}
            />
          ) : (
            <p>Preview HTML</p>
          )}
        </div>
      </div>
    </>
  )
}

export default App
