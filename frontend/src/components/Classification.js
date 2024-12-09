import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Classification = () => {
    const { employeeId } = useParams();
    const [employee, setEmployee] = useState(null);
    const [classification, setClassification] = useState(null);

    useEffect(() => {
        const fetchEmployeeData = async () => {
            try {
                const response = await axios.get(`/api/employee/${employeeId}/classify`);
                setEmployee(response.data.employee);
                setClassification(response.data.classification);
            } catch (error) {
                console.error("Error fetching classification:", error);
            }
        };
        fetchEmployeeData();
    }, [employeeId]);

    return (
        <div className="classification">
            {employee && (
                <div>
                    <h2>Classification for {employee.name}</h2>
                    <p><strong>Employee ID:</strong> {employee.employee_id}</p>
                    <p><strong>Performance Classification:</strong> {classification ? classification.label : 'Loading...'}</p>
                    <p><strong>Confidence:</strong> {classification ? classification.confidence : 'Loading...'}</p>
                </div>
            )}
        </div>
    );
};

export default Classification;
