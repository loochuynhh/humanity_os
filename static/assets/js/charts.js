// Task Chart
function initTaskChart(data) {
    const taskCtx = document.getElementById("taskChart").getContext("2d");
    new Chart(taskCtx, {
      type: "doughnut",
      data: {
        labels: ["To-do", "Đang làm", "Hoàn thành"],
        datasets: [{
          data: data,
          backgroundColor: ["#0d6efd", "#ffc107", "#198754"],
          borderWidth: 1
        }]
      },
      options: { 
        plugins: { 
          legend: { position: "bottom" },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value / total) * 100);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        },
        cutout: '65%'
      }
    });
  }
  
  // Time Chart
  function initTimeChart(data) {
    const timeCtx = document.getElementById("timeChart").getContext("2d");
    new Chart(timeCtx, {
      type: "line",
      data: {
        labels: ["T2", "T3", "T4", "T5", "T6", "T7", "CN"],
        datasets: [{
          label: "Giờ làm",
          data: data,
          borderColor: "#0d6efd",
          backgroundColor: "rgba(13, 110, 253, 0.1)",
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointBackgroundColor: "#0d6efd",
          pointRadius: 4
        }]
      },
      options: { 
        scales: { 
          y: { 
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return value + 'h';
              }
            }
          } 
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.parsed.y.toFixed(1) + ' giờ';
              }
            }
          }
        }
      }
    });
  }
  
  // KPI Trend Chart
  function initKpiTrendChart() {
    const kpiTrendCtx = document.getElementById("kpiTrendChart").getContext("2d");
    new Chart(kpiTrendCtx, {
      type: "bar",
      data: {
        labels: ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6"],
        datasets: [{
          label: "Điểm KPI",
          data: [75, 82, 78, 85, 88, 90],
          backgroundColor: "rgba(25, 135, 84, 0.7)",
          borderColor: "rgba(25, 135, 84, 1)",
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false,
            min: 50,
            max: 100,
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.parsed.y + '%';
              }
            }
          }
        }
      }
    });
  }
  
  // Productivity Chart
  function initProductivityChart() {
    const productivityCtx = document.getElementById("productivityChart").getContext("2d");
    new Chart(productivityCtx, {
      type: "radar",
      data: {
        labels: ["Sáng (8-12h)", "Chiều (12-17h)", "Tối (17-21h)", "Đêm (21-24h)"],
        datasets: [{
          label: "Năng suất",
          data: [85, 92, 78, 45],
          backgroundColor: "rgba(13, 110, 253, 0.2)",
          borderColor: "rgba(13, 110, 253, 1)",
          pointBackgroundColor: "rgba(13, 110, 253, 1)",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgba(13, 110, 253, 1)"
        }]
      },
      options: {
        scales: {
          r: {
            angleLines: {
              display: true
            },
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            }
          }
        }
      }
    });
  }
  
  // Performance Chart
  function initPerformanceChart(labels, data) {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Điểm hiệu suất',
          data: data,
          borderColor: '#4e73df',
          backgroundColor: 'rgba(78, 115, 223, 0.05)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }
  
  // Task Distribution Chart
  function initTaskDistributionChart(labels, data) {
    const ctx = document.getElementById('taskDistributionChart').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'],
          hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#dda20a'],
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        cutout: '70%',
        plugins: {
          legend: {
            position: 'right'
          }
        }
      }
    });
  }
  
  // Geolocation for Check-in/Check-out
  function initGeolocation() {
    function getLocation(inputId) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            document.getElementById(inputId).value = `${lat},${lon}`;
          },
          function(error) {
            alert('Không thể lấy vị trí: ' + error.message);
          }
        );
      } else {
        alert('Trình duyệt của bạn không hỗ trợ lấy vị trí.');
      }
    }
  
    const checkInModal = document.getElementById('checkInModal');
    if (checkInModal) {
      checkInModal.addEventListener('shown.bs.modal', function() {
        getLocation('checkin_location');
      });
    }
  
    const checkOutModal = document.getElementById('checkOutModal');
    if (checkOutModal) {
      checkOutModal.addEventListener('shown.bs.modal', function() {
        getLocation('checkout_location');
      });
    }
  }
  
  // Initialize charts and geolocation
  document.addEventListener('DOMContentLoaded', function() {
    // Lấy dữ liệu từ thuộc tính data attributes
    const taskChartElement = document.getElementById('taskChart');
    const timeChartElement = document.getElementById('timeChart');
    const performanceChartElement = document.getElementById('performanceChart');
    const taskDistributionChartElement = document.getElementById('taskDistributionChart');
  
    if (taskChartElement && taskChartElement.dataset.chartData) {
      initTaskChart(JSON.parse(taskChartElement.dataset.chartData));
    }
    if (timeChartElement && timeChartElement.dataset.chartData) {
      initTimeChart(JSON.parse(timeChartElement.dataset.chartData));
    }
    if (performanceChartElement && performanceChartElement.dataset.labels && performanceChartElement.dataset.chartData) {
      initPerformanceChart(
        JSON.parse(performanceChartElement.dataset.labels),
        JSON.parse(performanceChartElement.dataset.chartData)
      );
    }
    if (taskDistributionChartElement && taskDistributionChartElement.dataset.labels && taskDistributionChartElement.dataset.chartData) {
      initTaskDistributionChart(
        JSON.parse(taskDistributionChartElement.dataset.labels),
        JSON.parse(taskDistributionChartElement.dataset.chartData)
      );
    }
    initKpiTrendChart();
    initProductivityChart();
    initGeolocation();
  });