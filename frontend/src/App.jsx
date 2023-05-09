import React from 'react'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { format } from 'date-fns'
import './App.css'
import Trabajadores from './components/Trabajadores/Trabajadores'

const baseUrl = "http://127.0.0.1:5000"

function App() {

  const [description, setDescription] = useState("")
  const[eventsList, setEventsList] = useState([])

  const fetchEvents = async (e) =>{
    e.preventDefault()
    try{
      const data = await axios.get(`${baseUrl}/events`, {description})
      setEventsList([...eventsList, data.data])
      setDescription('')
      const { events } = data.data
      setEventsList(events)
    } catch(err){
      console.error(err.message)
    }
  }

  const handleChange = e => {
    setDescription(e.target.value)
  }

  const handleSubmit = e =>{
    e.preventDefault()
    console.log(description)
  }

  useEffect(() => {
    fetchEvents()
  }, [])
  
  return (
      <div className="App">
        <section>
          <form onSubmit={handleSubmit}>
            <label htmlFor="description">Description</label>
            <input onChange={handleChange} type="text" name="description" id="description" value={description}/>
            <button type="submit">Submit</button>
          </form>
        </section>
        <section>
          <ul>
            {eventsList.map(event => {
              return(
                <li key={event.id}>{event.description}</li>
              )
            })}
          </ul>
        </section>
      </div>
  )
}

export default App
