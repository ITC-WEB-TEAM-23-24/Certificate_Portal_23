import './assets/css/App.css';
import React, { useState, useEffect } from 'react';
import {Routes, Route, BrowserRouter} from "react-router-dom"

import Footer from './component/footer';
import Pg1 from './component/pg1';
import Pg2 from "./component/pg2";
import Pg3 from "./component/pg3";
import Pg4 from "./component/pg4";
import Login from "./component/login";
import Auth from './component/auth';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/0" element={<Auth/>} />
        <Route path="/1" element={<Pg1/>} />
        <Route path="/2" element={<Pg2/>} />
        <Route path="/3" element={<Pg3/>} />
        <Route path="/4" element={<Pg4/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
