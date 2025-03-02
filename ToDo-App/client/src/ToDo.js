// src/ToDo.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Spinner from './Spinner'; // Import Spinner component

const ToDo = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [points, setPoints] = useState(0);

  // Fetch tasks from the API
  const fetchTasks = async () => {
    try {
      const response = await axios.get('http://34.227.109.255:5000/Tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  // Add a new task
  const addTask = async () => {
    if (!newTask) return;

    const taskId = tasks.length ? tasks[tasks.length - 1].id + 1 : 1; // Simple ID generation
    const task = { id: taskId, Task: newTask };

    try {
      await axios.post('http://34.227.109.255:5000/Tasks', task);
      setNewTask('');
      fetchTasks(); // Refresh the task list
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  // Delete a task
  const deleteTask = async (id) => {
    try {
      await axios.delete(`http://34.227.109.255:5000/Tasks/${id}`);
      fetchTasks(); // Refresh the task list
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // Handle task completion
  const handleTaskCompletion = (id) => {
    setPoints(points + 1); // Increment points
    deleteTask(id); // Delete the task after completion
  };

  // Handle spinning
  const handleSpin = () => {
    setPoints(points - 1); // Deduct points for spinning
  };

  useEffect(() => {
    fetchTasks(); // Fetch tasks on component mount
  }, []);

  return (
    <div>
      <h1>To-Do List</h1>
      <input
        type="text"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
        placeholder="Add a new task"
      />
      <button onClick={addTask}>Add Task</button>
      <h2>Your Points: {points}</h2>
      <Spinner points={points} onSpin={handleSpin} />
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <input
              type="checkbox"
              onChange={() => handleTaskCompletion(task.id)}
            />
            {task.Task}
            <button onClick={() => deleteTask(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ToDo;