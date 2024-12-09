import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [stats, setStats] = useState({
        exceedsExpectations: 0,
        fullyMeetsExpectations: 0,
        needsImprovement: 0,
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('/api/dashboard/stats');
                setStats(response.data);
            } catch (error) {
                console.error("Error fetching stats:", error);
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="dashboard">
            <h2>Employee Performance Dashboard</h2>
            <div className="stats">
                <p><strong>Exceeds Expectations:</strong> {stats.exceedsExpectations}</p>
                <p><strong>Fully Meets Expectations:</strong> {stats.fullyMeetsExpectations}</p>
                <p><strong>Needs Improvement:</strong> {stats.needsImprovement}</p>
            </div>
        </div>
    );
};

export default Dashboard;
