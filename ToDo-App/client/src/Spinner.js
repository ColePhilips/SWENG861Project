// src/Spinner.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import CSS for styling

const Spinner = ({ points, onSpin }) => {
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);
  const [monsters, setMonsters] = useState([]);

  useEffect(() => {
    const fetchMonsters = async () => {
      try {
        const response = await axios.get('http://34.227.109.255:5000/Monsters');
        setMonsters(response.data);
      } catch (error) {
        console.error('Error fetching monsters:', error);
      }
    };

    fetchMonsters();
  }, []);

  const handleSpin = () => {
    if (points <= 0) return;

    setSpinning(true);
    onSpin();

    setTimeout(() => {
      const randomIndex = Math.floor(Math.random() * monsters.length);
      const selectedMonster = monsters[randomIndex];
      setResult(selectedMonster);
      setSpinning(false);
    }, 2000);
  };

  return (
    <div>
      <button className="spinner-button" onClick={handleSpin} disabled={spinning}>
        {spinning ? 'Spinning...' : 'Spin the Wheel!'}
      </button>
      {result && <h2>You got monster: {result.name} (ID: {result.id})!</h2>}
    </div>
  );
};

export default Spinner;