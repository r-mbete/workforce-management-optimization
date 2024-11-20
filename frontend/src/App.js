import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import Employees from './components/Employees/Employees';
import Prediction from './components/Prediction/Prediction';

const App = () => {
  return (
    <Router>
      <div className="App">
        <h1>Workforce Management System</h1>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/employees/:employeeId/prediction" element={<Prediction />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
