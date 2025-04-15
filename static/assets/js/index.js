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
                        label: function (context) {
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
                        callback: function (value) {
                            return value + 'h';
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
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
                        callback: function (value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
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
                        callback: function (value) {
                            return value + '%';
                        }
                    }
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
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    document.getElementById(inputId).value = `${lat},${lon}`;
                },
                function (error) {
                    alert('Không thể lấy vị trí: ' + error.message);
                }
            );
        } else {
            alert('Trình duyệt của bạn không hỗ trợ lấy vị trí.');
        }
    }

    const checkInModal = document.getElementById('checkInModal');
    if (checkInModal) {
        checkInModal.addEventListener('shown.bs.modal', function () {
            getLocation('checkin_location');
        });
    }

    const checkOutModal = document.getElementById('checkOutModal');
    if (checkOutModal) {
        checkOutModal.addEventListener('shown.bs.modal', function () {
            getLocation('checkout_location');
        });
    }
}

// Initialize charts and geolocation
document.addEventListener('DOMContentLoaded', function () {
    // Lấy dữ liệu từ thuộc tính data attributes
    const taskChartElement = document.getElementById('taskChart');
    const timeChartElement = document.getElementById('timeChart');

    if (taskChartElement && taskChartElement.dataset.chartData) {
        initTaskChart(JSON.parse(taskChartElement.dataset.chartData));
    }
    if (timeChartElement && timeChartElement.dataset.chartData) {
        initTimeChart(JSON.parse(timeChartElement.dataset.chartData));
    }

    initKpiTrendChart();
    initProductivityChart();
    initGeolocation();
});

document.addEventListener('DOMContentLoaded', function () {
    // Hàm hiển thị lỗi
    function showError(errorDivId, message) {
        const errorDiv = document.getElementById(errorDivId);
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.remove('d-none');
            setTimeout(() => errorDiv.classList.add('d-none'), 5000);
        }
    }

    // Hàm khởi tạo webcam
    function setupWebcam(modalId, videoId, canvasId, snapButtonId, imageDataId, previewId, submitButtonId, loadingId) {
        const modal = document.getElementById(modalId);
        const video = document.getElementById(videoId);
        const canvas = document.getElementById(canvasId);
        const snapButton = document.getElementById(snapButtonId);
        const imageDataInput = document.getElementById(imageDataId);
        const previewImg = document.getElementById(previewId);
        const submitButton = document.getElementById(submitButtonId);
        const loading = document.getElementById(loadingId);
        let stream = null;

        if (!modal || !video || !canvas || !snapButton || !imageDataInput || !previewImg || !submitButton || !loading) {
            console.error('Một hoặc nhiều phần tử không tồn tại trong setupWebcam:', { modalId, videoId, canvasId, snapButtonId, imageDataId, previewId, submitButtonId, loadingId });
            return;
        }

        modal.addEventListener('shown.bs.modal', () => {
            loading.style.display = 'block';
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(s => {
                    stream = s;
                    video.srcObject = stream;
                    loading.style.display = 'none';
                })
                .catch(err => {
                    loading.style.display = 'none';
                    showError(modalId + '_error', 'Không thể truy cập webcam: ' + err.message);
                });
        });

        modal.addEventListener('hidden.bs.modal', () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            video.srcObject = null;
            previewImg.classList.add('d-none');
            imageDataInput.value = '';
            snapButton.classList.remove('btn-success');
            snapButton.classList.add('btn-secondary');
            submitButton.disabled = true;
        });

        snapButton.addEventListener('click', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7);
            imageDataInput.value = compressedDataUrl;
            previewImg.src = compressedDataUrl;
            previewImg.classList.remove('d-none');

            snapButton.classList.remove('btn-secondary');
            snapButton.classList.add('btn-success');
            const locationInput = document.getElementById(modalId === 'checkInModal' ? 'checkin_location' : 'checkout_location');
            submitButton.disabled = !imageDataInput.value || !locationInput?.value;
        });
    }

    // Hàm lấy vị trí
    function setupGeolocation(modalId, inputId, loadingId) {
        const modal = document.getElementById(modalId);
        const input = document.getElementById(inputId);
        const loading = document.getElementById(loadingId);
        const submitButton = document.getElementById(modalId + '_submit');

        if (!modal || !input || !loading || !submitButton) {
            console.error('Một hoặc nhiều phần tử không tồn tại trong setupGeolocation:', { modalId, inputId, loadingId });
            return;
        }

        modal.addEventListener('shown.bs.modal', () => {
            if (navigator.geolocation) {
                loading.classList.remove('d-none');
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        input.value = `${lat},${lon}`;
                        loading.classList.add('d-none');
                        const imageDataInput = document.getElementById(modalId === 'checkInModal' ? 'checkin_image_data' : 'checkout_image_data');
                        submitButton.disabled = !input.value || !imageDataInput?.value;
                    },
                    error => {
                        loading.classList.add('d-none');
                        showError(modalId + '_error', 'Không thể lấy vị trí: ' + error.message);
                    }
                );
            } else {
                showError(modalId + '_error', 'Trình duyệt không hỗ trợ lấy vị trí.');
            }
        });
    }

    // Khởi tạo check-in
    if (document.getElementById('checkInModal')) {
        setupWebcam(
            'checkInModal',
            'checkin_video',
            'checkin_canvas',
            'checkin_snap',
            'checkin_image_data',
            'checkin_preview',
            'checkin_submit',
            'checkin_loading'
        );
        setupGeolocation('checkInModal', 'checkin_location', 'checkin_location_loading');
    }

    // Khởi tạo check-out
    if (document.getElementById('checkOutModal')) {
        setupWebcam(
            'checkOutModal',
            'checkout_video',
            'checkout_canvas',
            'checkout_snap',
            'checkout_image_data',
            'checkout_preview',
            'checkout_submit',
            'checkout_loading'
        );
        setupGeolocation('checkOutModal', 'checkout_location', 'checkout_location_loading');
    }
});