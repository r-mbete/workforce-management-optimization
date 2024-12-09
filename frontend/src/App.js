import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './components/Dashboard/Dashboard';
import Employees from './components/Employees/Employees';
import ClassifyPerformance from './components/ClassifyPerformance/ClassifyPerformance'; // Updated component

const App = () => {
  return (
    <Router>
      <div className="App">
        <h1>Workforce Management System</h1>
        {/* Add links for navigation */}
        <nav>
          <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/employees">Employees</a></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/employees" element={<Employees />} />
          {/* Updated to reflect classification instead of prediction */}
          <Route path="/employees/:employeeId/classify" element={<ClassifyPerformance />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
