import React, { useState } from 'react';
import axios from 'axios';

const Employees = () => {
    const [employeeData, setEmployeeData] = useState({
        employee_id: '',
        name: '',
        age: '',
        gender: '',
        education_level: '',
        job_role: '',
        years_experience: '',
    });

    const handleChange = (e) => {
        setEmployeeData({
            ...employeeData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/employee', employeeData);
            if (response.data.status === 'success') {
                alert('Employee added successfully!');
            }
        } catch (error) {
            console.error("Error adding employee:", error);
            alert('Error adding employee!');
        }
    };

    return (
        <div className="employee-form">
            <h2>Add Employee</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="employee_id"
                    placeholder="Employee ID"
                    value={employeeData.employee_id}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="name"
                    placeholder="Name"
                    value={employeeData.name}
                    onChange={handleChange}
                    required
                />
                <input
                    type="number"
                    name="age"
                    placeholder="Age"
                    value={employeeData.age}
                    onChange={handleChange}
                    required
                />
                <select
                    name="gender"
                    value={employeeData.gender}
                    onChange={handleChange}
                    required
                >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>
                <input
                    type="text"
                    name="education_level"
                    placeholder="Education Level"
                    value={employeeData.education_level}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="job_role"
                    placeholder="Job Role"
                    value={employeeData.job_role}
                    onChange={handleChange}
                    required
                />
                <input
                    type="number"
                    name="years_experience"
                    placeholder="Years of Experience"
                    value={employeeData.years_experience}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Add Employee</button>
            </form>
        </div>
    );
};

export default Employees;
