import React from 'react'
import { Link } from 'react-router-dom'
import i1 from "../assets/img/home.png"
import Footer from './footer'

function Layout(props) {
  const data = JSON.parse(localStorage.getItem('project_data'))
  return (
    <div className='app container'>
      <div className='pg0 container'>
            <header> Institure Technical Council</header>
                <div className='text'>
                <h1>Welcome to the Certicate Portal</h1>
                <p>{data.name} Download Your Certificates Here</p>
            </div>
            <div className='img-div'>
                <img src={i1} alt="Home image" srcSet="" />
            </div>
        </div>         
        <div className='pg'>
            {props.children}
        </div>
      <Footer/>
    </div>
  )
}
export default Layout