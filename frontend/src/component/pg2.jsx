import React, { useState, useEffect } from 'react';
import gif from "../assets/img/gif.webp";
import { Link } from 'react-router-dom';
import Layout from './layout';
import axios from 'axios';

function Pg2() {
  const [isMentee, setIsMentee] = useState(false);
  const [isMentor, setIsMentor] = useState(false);
  const data = JSON.parse(localStorage.getItem('project_data'));
  const [menteeUrl, setMenteeUrl] = useState('/4');
  const [mentorUrl, setMentorUrl] = useState('/4');

  useEffect(() => {
    const checkRoles = async (rollNumber) => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/kritika/${rollNumber}`);
        setIsMentee(response.data.is_mentee);
        setIsMentor(response.data.is_mentor);

        // Update URL variables based on the flag value
        if (response.data.is_mentee){
          setMenteeUrl('/3');
        }

        if (response.data.is_mentor){
          setMentorUrl('/3');
        }

      } catch (error) {
        console.error('Error:', error);
      }
    };

    checkRoles(data.roll_number);
  }, [data.roll_number]); // Include data.roll_number in the dependency array

  return (
    <Layout>
      <Link to={"/1"}><i></i></Link>
      <h2>For which position do you want a certificate?</h2>
      <img src={gif} alt="" srcSet="" />
      <div className='box-wrapper'>
        <Link to={menteeUrl} className='boxes'><div className='box'>Mentee</div></Link>
        <Link to={mentorUrl} className='boxes'><div className='box'>Mentor</div></Link>
      </div>
    </Layout>
  );
}

export default Pg2;
