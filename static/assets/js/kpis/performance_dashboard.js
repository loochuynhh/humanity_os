document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('kpiChart').getContext('2d');
    const chartLabels = {{ kpi_chart_data.labels|safe }} || [];
    const chartDataValues = {{ kpi_chart_data.data|safe }} || [];

    // Điều chỉnh kích thước biểu đồ dựa trên số KPI
    const kpiCount = chartLabels.length;
    const chartWidth = kpiCount < 10 ? 400 : Math.min(kpiCount * 50, 1200);
    ctx.canvas.style.width = `${chartWidth}px`;
    ctx.canvas.style.maxWidth = '100%';

    const chartData = {
        labels: chartLabels,
        datasets: [{
            label: 'Tỷ lệ đạt (%)',
            data: chartDataValues,
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 2,
            hoverBackgroundColor: 'rgba(0, 123, 255, 0.8)',
        }]
    };

    const chart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 200,
                    grid: {
                        color: '#e9ecef',
                    },
                    ticks: {
                        font: {
                            size: 12,
                        },
                    },
                    title: {
                        display: true,
                        text: 'Tỷ lệ đạt (%)',
                        font: {
                            size: 14,
                            weight: 'bold',
                        },
                    },
                },
                x: {
                    grid: {
                        display: false,
                    },
                    ticks: {
                        font: {
                            size: 12,
                        },
                        maxRotation: kpiCount < 10 ? 0 : 45,
                        minRotation: kpiCount < 10 ? 0 : 45,
                    },
                    title: {
                        display: true,
                        text: 'KPI',
                        font: {
                            size: 14,
                            weight: 'bold',
                        },
                    },
                },
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                        },
                    },
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                    },
                    bodyFont: {
                        size: 12,
                    },
                    callbacks: {
                        label: function(context) {
                            return `Tỷ lệ: ${context.parsed.y.toFixed(2)}%`;
                        },
                    },
                },
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart',
            },
        },
    });

    // Generate base64 image for PDF
    setTimeout(() => {
        const base64Image = chart.toBase64Image();
        window.kpiChartBase64 = base64Image;
    }, 1000);
});