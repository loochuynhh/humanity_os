/**
 * Admin Dashboard JavaScript
 * 
 * Handle charts and features for admin dashboard
 */

// Chart instances
let usersChart, taskStatusChart, projectStatusChart, performanceChart;

/**
 * Initialize user growth chart
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Month labels
 * @param {Array} data - User count data
 */
function initUsersChart(canvasId, labels, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  if (usersChart) usersChart.destroy(); // Destroy previous chart if exists
  
  usersChart = new Chart(context, {
    type: 'line',
    data: {
      labels: labels || [],
      datasets: [{
        label: 'New Users',
        data: data || [],
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        borderColor: '#0d6efd',
        borderWidth: 2,
        tension: 0.4,
        pointBackgroundColor: '#0d6efd',
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            boxWidth: 20,
            usePointStyle: true
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          titleFont: {
            size: 14
          },
          bodyFont: {
            size: 13
          },
          callbacks: {
            label: function(context) {
              return `New users: ${context.parsed.y}`;
            }
          }
        }
      }
    }
  });
}

/**
 * Initialize task status distribution chart
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Status labels
 * @param {Array} data - Task count data
 * @param {Array} colors - Chart colors
 */
function initTaskStatusChart(canvasId, labels, data, colors) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  if (taskStatusChart) taskStatusChart.destroy(); // Destroy previous chart if exists
  
  taskStatusChart = new Chart(context, {
    type: 'doughnut',
    data: {
      labels: labels || [],
      datasets: [{
        data: data || [],
        backgroundColor: colors || ['#0d6efd', '#ffc107', '#198754'],
        borderColor: colors || ['#0d6efd', '#ffc107', '#198754'],
        borderWidth: 1,
        hoverOffset: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            boxWidth: 12,
            usePointStyle: true,
            padding: 20,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed || 0;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        }
      },
      cutout: '60%'
    }
  });
}

/**
 * Initialize project status chart
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Project status labels
 * @param {Array} data - Project count data
 * @param {Array} colors - Chart colors
 */
function initProjectStatusChart(canvasId, labels, data, colors) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  if (projectStatusChart) projectStatusChart.destroy(); // Destroy previous chart if exists
  
  projectStatusChart = new Chart(context, {
    type: 'pie',
    data: {
      labels: labels || [],
      datasets: [{
        data: data || [],
        backgroundColor: colors || ['#0d6efd', '#198754'],
        borderColor: colors || ['#0d6efd', '#198754'],
        borderWidth: 1,
        hoverOffset: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            boxWidth: 12,
            usePointStyle: true,
            padding: 20
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed || 0;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

/**
 * Initialize performance metrics chart
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Performance categories
 * @param {Array} data - KPI count data
 * @param {Array} colors - Chart colors
 */
function initPerformanceChart(canvasId, labels, data, colors) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  if (performanceChart) performanceChart.destroy(); // Destroy previous chart if exists
  
  performanceChart = new Chart(context, {
    type: 'bar',
    data: {
      labels: labels || [],
      datasets: [{
        label: 'KPI Count',
        data: data || [],
        backgroundColor: colors || ['#198754', '#ffc107', '#dc3545'],
        borderColor: colors || ['#198754', '#ffc107', '#dc3545'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed.y || 0;
              const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `KPIs: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

/**
 * Animate counter effects for statistics cards
 */
function initCounterAnimation() {
  const numbers = document.querySelectorAll('.numbers h5');
  if (!numbers || numbers.length === 0) return;
  
  numbers.forEach(number => {
    const finalValue = parseFloat(number.textContent.replace(/[^0-9.-]+/g, ''));
    
    if (!isNaN(finalValue)) {
      // Only animate for numbers greater than 10
      if (finalValue > 10) {
        number.textContent = '0';
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 25); // 25 steps
        const timer = setInterval(() => {
          currentValue += increment;
          if (currentValue >= finalValue) {
            currentValue = finalValue;
            clearInterval(timer);
          }
          
          // Handle percentage values
          if (number.textContent.includes('%')) {
            number.textContent = currentValue.toFixed(1) + '%';
          } else {
            number.textContent = Math.round(currentValue).toLocaleString();
          }
        }, 40);
      }
    }
  });
}

/**
 * Add animation effect for progress bars
 */
function initProgressBars() {
  const progressBars = document.querySelectorAll('.progress-bar');
  if (!progressBars || progressBars.length === 0) return;
  
  progressBars.forEach(bar => {
    // Start with zero width
    bar.style.width = '0%';
    
    // Short timeout to ensure animation works
    setTimeout(() => {
      // Get value from aria-valuenow attribute
      const value = bar.getAttribute('aria-valuenow');
      // Set width based on value
      bar.style.width = `${value}%`;
    }, 100);
  });
}

/**
 * Initialize all dashboard scripts when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
  // Check if we're on the admin dashboard page
  const isDashboardPage = document.querySelector('.container-fluid .row .card .numbers') !== null;
  if (!isDashboardPage) return;
  
  console.log('Initializing admin dashboard...');
  
  try {
    // Initialize counter animations
    initCounterAnimation();
    
    // Initialize progress bar animations
    initProgressBars();
    
    // Initialize charts if canvas elements exist and data is available
    if (document.getElementById('users-chart')) {
      try {
        const chartData = typeof userChartData !== 'undefined' ? userChartData : { labels: [], data: [] };
        initUsersChart('users-chart', 
          chartData.labels || [], 
          chartData.data || []
        );
        console.log('Users chart initialized');
      } catch (e) {
        console.error('Error initializing users chart:', e);
      }
    }
    
    if (document.getElementById('task-status-chart')) {
      try {
        const chartData = typeof taskChartData !== 'undefined' ? taskChartData : { labels: [], data: [], colors: [] };
        initTaskStatusChart('task-status-chart', 
          chartData.labels || [], 
          chartData.data || [], 
          chartData.colors || []
        );
        console.log('Task status chart initialized');
      } catch (e) {
        console.error('Error initializing task status chart:', e);
      }
    }
    
    if (document.getElementById('project-status-chart')) {
      try {
        const chartData = typeof projectChartData !== 'undefined' ? projectChartData : { labels: [], data: [], colors: [] };
        initProjectStatusChart('project-status-chart',
          chartData.labels || [],
          chartData.data || [],
          chartData.colors || []
        );
        console.log('Project status chart initialized');
      } catch (e) {
        console.error('Error initializing project status chart:', e);  
      }
    }
    
    if (document.getElementById('performance-chart')) {
      try {
        const chartData = typeof performanceChartData !== 'undefined' ? performanceChartData : { labels: [], data: [], colors: [] };
        initPerformanceChart('performance-chart',
          chartData.labels || [],
          chartData.data || [],
          chartData.colors || []
        );
        console.log('Performance chart initialized');
      } catch (e) {
        console.error('Error initializing performance chart:', e);
      }
    }
    
    console.log('Admin dashboard initialization complete');
  } catch (e) {
    console.error('Error during dashboard initialization:', e);
  }
}); 