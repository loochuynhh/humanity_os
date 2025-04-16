/**
 * Initialize Task Chart (Doughnut)
 * Expects data: [To_do, In_progress, Completed]
 */
function initTaskChart(data) {
    const taskCtx = document.getElementById("taskChart").getContext("2d");
    const chartData = Array.isArray(data) && data.length >= 3 ? data.slice(0, 3) : [0, 0, 0];
    new Chart(taskCtx, {
        type: "doughnut",
        data: {
            labels: ["To-do", "Đang làm", "Hoàn thành"],
            datasets: [{
                data: chartData,
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
                            const percentage = total ? Math.round((value / total) * 100) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

/**
 * Initialize Time Chart (Line)
 * Expects data: [hours for Mon, Tue, Wed, Thu, Fri, Sat, Sun]
 */
function initTimeChart(data) {
    const timeCtx = document.getElementById("timeChart").getContext("2d");
    const chartData = Array.isArray(data) && data.length === 7 ? data : [0, 0, 0, 0, 0, 0, 0];
    new Chart(timeCtx, {
        type: "line",
        data: {
            labels: ["T2", "T3", "T4", "T5", "T6", "T7", "CN"],
            datasets: [{
                label: "Giờ làm",
                data: chartData,
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

/**
 * Initialize Project Time Allocation Chart (Pie)
 * Expects data: { labels: [project_name, ...], data: [hours, ...] }
 */
function initProjectTimeChart(data) {
    const projectTimeCtx = document.getElementById("projectTimeChart").getContext("2d");
    const chartData = data && data.labels && data.data ? {
        labels: data.labels.length ? data.labels : ['Không có dự án'],
        data: data.data.length ? data.data : [1]
    } : {
        labels: ['Không có dự án'],
        data: [1]
    };
    new Chart(projectTimeCtx, {
        type: "pie",
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.data,
                backgroundColor: ["#0d6efd", "#ffc107", "#198754", "#dc3545", "#6f42c1"],
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
                            const percentage = total ? Math.round((value / total) * 100) : 0;
                            return `${label}: ${value.toFixed(1)}h (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize Goals Progress Chart (Horizontal Bar)
 * Expects data: { labels: [goal_name, ...], data: [percentage, ...] }
 */
function initGoalsProgressChart(data) {
    const goalsProgressCtx = document.getElementById("goalsProgressChart").getContext("2d");
    const chartData = data && data.labels && data.data ? {
        labels: data.labels.length ? data.labels : ['Không có mục tiêu'],
        data: data.data.length ? data.data : [0]
    } : {
        labels: ['Không có mục tiêu'],
        data: [0]
    };

    // Giới hạn độ dài nhãn để kiểm soát chiều rộng
    const maxLabelLength = 15;
    const truncatedLabels = chartData.labels.map(label => 
        label.length > maxLabelLength ? label.substring(0, maxLabelLength - 3) + '...' : label
    );

    new Chart(goalsProgressCtx, {
        type: "bar",
        data: {
            labels: truncatedLabels,
            datasets: [{
                label: "Tiến độ (%)",
                data: chartData.data,
                backgroundColor: "rgba(25, 135, 84, 0.7)",
                borderColor: "rgba(25, 135, 84, 1)",
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                y: {
                    ticks: {
                        maxRotation: 0, // Buộc nhãn ngang
                        minRotation: 0,
                        autoSkip: false // Đảm bảo hiển thị tất cả nhãn
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            // Hiển thị đầy đủ tên mục tiêu và phần trăm
                            const fullLabel = chartData.labels[context.dataIndex];
                            return `${fullLabel}: ${context.parsed.x}%`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Show error message in modal
 */
function showError(errorDivId, message) {
    const errorDiv = document.getElementById(errorDivId);
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
        setTimeout(() => errorDiv.classList.add('d-none'), 5000);
    }
}

/**
 * Setup webcam for check-in/check-out
 */
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
        console.error('Thiếu phần tử trong setupWebcam:', { modalId, videoId, canvasId, snapButtonId, imageDataId, previewId, submitButtonId, loadingId });
        showError(modalId + '_error', 'Lỗi khởi tạo webcam. Vui lòng thử lại.');
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

/**
 * Setup geolocation for check-in/check-out
 */
function setupGeolocation(modalId, inputId, loadingId) {
    const modal = document.getElementById(modalId);
    const input = document.getElementById(inputId);
    const loading = document.getElementById(loadingId);
    const submitButtonId = modalId.toLowerCase().replace('modal', '_submit');
    const submitButton = document.getElementById(submitButtonId);

    if (!modal || !input || !loading || !submitButton) {
        console.error('Thiếu phần tử trong setupGeolocation:', { modalId, inputId, loadingId, submitButtonId });
        showError(modalId + '_error', 'Lỗi lấy vị trí. Vui lòng thử lại.');
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

/**
 * Initialize all charts and features
 */
document.addEventListener('DOMContentLoaded', function () {
    function initChart(elementId, initFunction, expectedType) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.warn(`Không tìm thấy phần tử ${elementId}`);
            return;
        }

        let chartData;
        if (elementId === 'projectTimeChart' || elementId === 'goalsProgressChart') {
            chartData = window.djangoChartData ? window.djangoChartData[elementId] : null;
        } else {
            chartData = element.dataset.chartData;
        }

        console.log(`${elementId} data:`, chartData);

        if (!chartData || (typeof chartData === 'string' && (chartData.trim() === '' || chartData === '{' || chartData === '{}'))) {
            console.warn(`Dữ liệu không hợp lệ hoặc rỗng cho ${elementId}`);
            initFunction(expectedType === 'array' ? [] : { labels: ['Không có dữ liệu'], data: [1] });
            return;
        }

        try {
            let parsedData;
            if (elementId === 'projectTimeChart' || elementId === 'goalsProgressChart') {
                parsedData = chartData;
            } else {
                parsedData = JSON.parse(chartData);
            }

            if (expectedType === 'object') {
                if (!parsedData || !parsedData.labels || !parsedData.data || !Array.isArray(parsedData.labels) || !Array.isArray(parsedData.data)) {
                    console.warn(`Dữ liệu object không đúng định dạng cho ${elementId}:`, parsedData);
                    initFunction({ labels: ['Không có dữ liệu'], data: [1] });
                    return;
                }
            }
            initFunction(parsedData);
        } catch (e) {
            console.error(`Lỗi parse dữ liệu cho ${elementId}:`, e.message, chartData);
            initFunction(expectedType === 'array' ? [] : { labels: ['Không có dữ liệu'], data: [1] });
        }
    }

    initChart('taskChart', initTaskChart, 'array');
    initChart('timeChart', initTimeChart, 'array');
    initChart('projectTimeChart', initProjectTimeChart, 'object');
    initChart('goalsProgressChart', initGoalsProgressChart, 'object');

    // Initialize webcam and geolocation
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
