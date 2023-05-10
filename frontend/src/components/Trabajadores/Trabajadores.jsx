import React from 'react'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { format } from 'date-fns'

const baseUrl = "http://127.0.0.1:5000"

function Trabajadores() {

  const [description, setDescription] = useState("")
  const[editDescription, setEditDescription] = useState("")
  const[eventsList, setEventsList] = useState([])
  const[eventId, setEventId] = useState(null)

  const fetchEvents = async () =>{
    try{
      const data = await axios.get(`${baseUrl}/events`, {description})
      setEventsList([...eventsList, data.data])
      setDescription('')
      const { events } = data.data
      setEventsList(events)
    } catch(err){
      console.log(err.message)
    }
    
  }

  const handleChange = (e, field) => {
    if (field === 'edit'){
      setEditDescription(e.target.value)
    } else{
      setDescription(e.target.value)
    }
  }

  const handleSubmit = async (e) =>{
    e.preventDefault()
    try{
      if (editDescription){
        const data = await axios.put(`${baseUrl}/events/${eventId}`, {description: editDescription}) 
        const updatedEvent = data.data.event
        const updatedList = eventsList.map(event => {
          if (event.id === eventId){
            return event = updatedEvent
          }
          return event
        })
        setEventsList(updatedList)
      } else{
        const data = await axios.post(`${baseUrl}/events`, {description})
        setEventsList([...eventsList, data.data])
      }
      setDescription('')
      setEditDescription('')
      setEventId(null)
    } catch(err){
      console.log(err.message)
    }
  }

  const handleDelete = async (id) =>{
    try{
      await axios.delete(`${baseUrl}/events/${id}`)
      const updatedList = eventsList.filter(event => event.id != id)
      setEventsList(updatedList)
    } catch(err){
      console.error(err.message)
    }
  }

  const toggleEdit = (event) => {
    setEventId(event.id)
    setEditDescription(event.description)
  }

  useEffect(() => {
    fetchEvents()
  }, [])
  
  return (
      <div className="App">
        <section>
          <form onSubmit={handleSubmit}>
            <label htmlFor="description">Description</label>
            <input onChange={(e) => handleChange(e, 'description')} type="text" name="description" id="description" placeholder='Describe the event' value={description}/>
            <button type="submit">Submit</button>
          </form>
        </section>
        <section>
        <ul>
          {eventsList.map(event => {
            if (eventId === event.id){
              return(
                <form onSubmit={handleSubmit} key={event.id}>                  
                  <input onChange={(e) => handleChange(e, 'edit')} type="text" name="editDescription" id="editDescription" value={editDescription} />
                  <button type='submit'>Submit</button>
                </form>
              )
            } else{
              return(
                  <li style={{display: "flex"}} key={event.id}>
                    {format(new Date(event.created_at), "MM/dd, p")}: {" "}
                    {event.description}
                    <button onClick={() => toggleEdit(event)}>Edit</button>
                    <button onClick={() => handleDelete(event.id)}>x</button>
                  </li>
              )
            }
          })}
          </ul>
        </section>
      </div>
  )
}

export default Trabajadores

/**import React from 'react';
import { useForm } from 'react-hook-form';
import './Trabajadores.css';

const Trabajadores = () => {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <div className="trabajadores-container">
      <h2>Trabajadores</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="trabajadores-form">
        <div className="trabajadores-input-container">
          <label htmlFor="nombre">Nombre:</label>
          <input type="text" id="nombre" {...register('nombre')} />
        </div>
        <div className="trabajadores-input-container">
          <label htmlFor="direccion">Dirección:</label>
          <input type="text" id="direccion" {...register('direccion')} />
        </div>
        <div className="trabajadores-input-container">
          <label htmlFor="edad">Edad:</label>
          <input type="text" id="edad" {...register('edad')} />
        </div>
        <div className="trabajadores-input-container">
          <label htmlFor="pais">País:</label>
          <select id="pais" {...register('pais')}>
            <option value="es">España</option>
            <option value="it">Italia</option>
            <option value="fr">Francia</option>
          </select>
        </div>
        <input type="submit" value="Enviar" className="trabajadores-submit-button" />
      </form>
    </div>
  );
};

export default Trabajadores;*/
