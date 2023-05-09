import React from 'react';
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

export default Trabajadores;
