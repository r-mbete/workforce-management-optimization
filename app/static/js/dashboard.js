// Fetch statistics from the backend API and render the chart
fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Fully Meet Expectations', 'Needs Improvement'],
                datasets: [{
                    label: 'Performance Statistics',
                    data: [data.high_performers, data.average_performers],
                    backgroundColor: ['#4361EE', '#3F8EFC'],
                    borderColor: ['#FFFFFF', '#FFFFFF'],
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        });
    });

