/**
 * Temperature Chart Handler
 * Creates and manages temperature charts using Chart.js
 */

/**
 * Create a temperature and humidity chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Array} timestamps - Array of timestamp strings
 * @param {Array} temperatures - Array of temperature values
 * @param {Array} humidities - Array of humidity values
 * @param {number} targetTemp - Target temperature
 * @param {number} minThreshold - Minimum temperature threshold
 * @param {number} maxThreshold - Maximum temperature threshold
 */
function createTemperatureChart(canvasId, timestamps, temperatures, humidities, targetTemp, minThreshold, maxThreshold) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Format timestamps for display
    const labels = timestamps.map(ts => {
        const date = new Date(ts);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // Create chart with dual Y axes
    const tempChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderWidth: 2,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    fill: false,
                    tension: 0.1,
                    yAxisID: 'y'
                },
                {
                    label: 'Humidity (%)',
                    data: humidities,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 2,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    fill: false,
                    tension: 0.1,
                    yAxisID: 'y1'
                },
                {
                    label: 'Target',
                    data: Array(timestamps.length).fill(targetTemp),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    yAxisID: 'y'
                },
                {
                    label: 'Min',
                    data: Array(timestamps.length).fill(minThreshold),
                    borderColor: 'rgba(54, 162, 235, 0.5)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    yAxisID: 'y'
                },
                {
                    label: 'Max',
                    data: Array(timestamps.length).fill(maxThreshold),
                    borderColor: 'rgba(255, 99, 132, 0.5)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            stacked: false,
            plugins: {
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return timestamps[context[0].dataIndex];
                        }
                    }
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        filter: function(item, chart) {
                            // Hide Min, Max, Target from legend
                            return !['Min', 'Max', 'Target'].includes(item.text);
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    grid: {
                        drawOnChartArea: false
                    },
                    suggestedMin: Math.min(minThreshold - 2, Math.min(...temperatures)),
                    suggestedMax: Math.max(maxThreshold + 2, Math.max(...temperatures))
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
    
    return tempChart;
}

/**
 * Create a door opening chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Array} timestamps - Array of timestamp strings
 * @param {Array} durations - Array of door open durations in seconds
 */
function createDoorOpeningChart(canvasId, timestamps, durations) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Format timestamps for display
    const labels = timestamps.map(ts => {
        const date = new Date(ts);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // Create chart
    const doorChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Door Open Duration (seconds)',
                data: durations,
                backgroundColor: 'rgba(255, 193, 7, 0.5)',
                borderColor: 'rgba(255, 193, 7, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return timestamps[context[0].dataIndex];
                        },
                        label: function(context) {
                            const seconds = context.raw;
                            if (seconds < 60) {
                                return `${seconds} seconds`;
                            } else {
                                const minutes = Math.floor(seconds / 60);
                                const remainingSecs = seconds % 60;
                                return `${minutes}m ${remainingSecs}s`;
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Duration (seconds)'
                    },
                    beginAtZero: true
                }
            }
        }
    });
    
    return doorChart;
}

/**
 * Update a chart with new data
 * @param {Chart} chart - Chart.js instance to update
 * @param {Array} timestamps - New timestamps
 * @param {Array} dataValues - New data values for the first dataset
 * @param {Array|null} secondaryValues - New data values for the second dataset (optional)
 */
function updateChart(chart, timestamps, dataValues, secondaryValues = null) {
    // Format timestamps for display
    const labels = timestamps.map(ts => {
        const date = new Date(ts);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // Update labels
    chart.data.labels = labels;
    
    // Update primary dataset
    chart.data.datasets[0].data = dataValues;
    
    // Update secondary dataset if provided
    if (secondaryValues && chart.data.datasets.length > 1) {
        chart.data.datasets[1].data = secondaryValues;
    }
    
    // Update reference lines for temperature chart
    if (chart.data.datasets.length >= 5) {
        // Target, Min, Max reference lines
        const targetTemp = chart.data.datasets[2].data[0];
        const minTemp = chart.data.datasets[3].data[0];
        const maxTemp = chart.data.datasets[4].data[0];
        
        chart.data.datasets[2].data = Array(timestamps.length).fill(targetTemp);
        chart.data.datasets[3].data = Array(timestamps.length).fill(minTemp);
        chart.data.datasets[4].data = Array(timestamps.length).fill(maxTemp);
    }
    
    // Update the chart
    chart.update();
}
