import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Prediction = () => {
    const { employeeId } = useParams();
    const [employee, setEmployee] = useState(null);
    const [prediction, setPrediction] = useState(null);

    useEffect(() => {
        const fetchEmployeeData = async () => {
            try {
                const response = await axios.get(`/api/employee/${employeeId}/predict`);
                setEmployee(response.data.employee);
                setPrediction(response.data.prediction);
            } catch (error) {
                console.error("Error fetching prediction:", error);
            }
        };
        fetchEmployeeData();
    }, [employeeId]);

    return (
        <div className="prediction">
            {employee && (
                <div>
                    <h2>Prediction for {employee.name}</h2>
                    <p><strong>Employee ID:</strong> {employee.employee_id}</p>
                    <p><strong>Performance Rating:</strong> {prediction ? prediction.rating : 'Loading...'}</p>
                    <p><strong>Confidence:</strong> {prediction ? prediction.confidence : 'Loading...'}</p>
                </div>
            )}
        </div>
    );
};

export default Prediction;
