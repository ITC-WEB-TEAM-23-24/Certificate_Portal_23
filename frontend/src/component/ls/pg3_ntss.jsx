// Pg3.jsx
import React from 'react';
import gif2 from "../../assets/img/gif4.gif";
import Layout from '../layout';
import { useLocation } from 'react-router-dom';

function Pg3_NTSS(){
  const data = JSON.parse(localStorage.getItem('project_data'));
  const url = localStorage.getItem('selectedOption');
  return (
    <Layout>
      <h2>Congratulations, You can download Certificate for NTSS</h2>
      <img src={gif2} alt="" srcSet="" className='dumb_img'/>
      <div className='box-wrapper pg3'>
        <div className='boxes'>
          <a
            href={`https://itc.gymkhana.iitb.ac.in/certificateBackend/download/ntss/${data.roll_number}`}
            className='box'
          > 
            Download Certificate
          </a>
        </div>
      </div>
    </Layout>
  );
}

export default Pg3_NTSS;
