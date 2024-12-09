import axios from 'axios';

// Add a new employee and classify their performance
export const addEmployee = async (employeeData) => {
    try {
        const response = await axios.post('/api/employee', employeeData); // Assuming your backend handles classification automatically
        return response.data;
    } catch (error) {
        console.error("Error adding employee:", error);
        throw error;
    }
};

// Get dashboard stats on employee performance classifications
export const getDashboardStats = async () => {
    try {
        const response = await axios.get('/api/dashboard/stats');
        return response.data;
    } catch (error) {
        console.error("Error fetching dashboard stats:", error);
        throw error;
    }
};

// Get the classification result for a specific employee
export const getClassification = async (employeeId) => {
    try {
        const response = await axios.get(`/api/employee/${employeeId}/classify`);
        return response.data;
    } catch (error) {
        console.error("Error fetching classification:", error);
        throw error;
    }
};

