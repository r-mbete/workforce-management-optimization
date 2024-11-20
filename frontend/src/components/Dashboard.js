import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [stats, setStats] = useState({
        highPerformers: 0,
        avgPerformers: 0,
        lowPerformers: 0,
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
                <p><strong>High Performers:</strong> {stats.highPerformers}</p>
                <p><strong>Average Performers:</strong> {stats.avgPerformers}</p>
                <p><strong>Low Performers:</strong> {stats.lowPerformers}</p>
            </div>
        </div>
    );
};

export default Dashboard;
