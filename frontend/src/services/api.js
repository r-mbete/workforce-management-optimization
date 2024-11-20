import axios from 'axios';

export const addEmployee = async (employeeData) => {
    try {
        const response = await axios.post('/api/employee', employeeData);
        return response.data;
    } catch (error) {
        console.error("Error adding employee:", error);
        throw error;
    }
};

export const getDashboardStats = async () => {
    try {
        const response = await axios.get('/api/dashboard/stats');
        return response.data;
    } catch (error) {
        console.error("Error fetching dashboard stats:", error);
        throw error;
    }
};

export const getPrediction = async (employeeId) => {
    try {
        const response = await axios.get(`/api/employee/${employeeId}/predict`);
        return response.data;
    } catch (error) {
        console.error("Error fetching prediction:", error);
        throw error;
    }
};
