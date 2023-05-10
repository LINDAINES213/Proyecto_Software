import React from 'react'
import './App.css'
//import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Trabajadores from './components/Trabajadores/Trabajadores'


function App() {

  return (
    <div>
      <Trabajadores />
    </div>
  )
}

export default App

/**<BrowserRouter>
      <Switch>
        <Route exact path="/" component={Inicio} />
        <Route path="/nosotros" component={Nosotros} />
        <Route path="/servicios" component={Servicios} />
        <Route path="/contacto" component={Contacto} />
      </Switch>
    </BrowserRouter> */
