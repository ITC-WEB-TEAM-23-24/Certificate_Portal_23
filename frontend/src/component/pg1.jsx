// Pg1.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import Layout from './layout';

function Pg1() {
  return (
    <Layout>
      <h2>A small selection of some recent events</h2>
      <p>
        It's been a wild ride since I've started out! I have worked with big and small brands from climate tech, fintech, business development, lifestyle, manufacturing, real estate and everything in between.
      </p>
      <div className='box-wrapper'>
        <Link to={{ pathname: "/2/ksp"}} className='boxes'>
          <div className='box'>Kritika Summer Project</div>
        </Link>
        <Link to={{ pathname: "/ls"}} className='boxes'>
          <div className='box'>Learner Space</div>
        </Link>
        <Link to={{ pathname: "/2/itsp"}} className='boxes'>
          <div className='box'>ITSP</div>
        </Link>
        <Link to={{ pathname: "/2/soc"}} className='boxes'>
          <div className='box'>Season of Code</div>
        </Link>
        <Link to={{ pathname: "/2/sos"}} className='boxes'>
          <div className='box'>Summer of Science</div>
        </Link>
      </div>
    </Layout>
  );
}

export default Pg1;
