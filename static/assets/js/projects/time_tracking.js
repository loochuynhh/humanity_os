$(document).ready(function() {
    // Thiết lập CSRF token cho AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Khởi tạo DataTable cho lịch sử time entries
    $('#timeEntriesTable').DataTable({
        "language": {
            "url": "/static/assets/js/plugin/datatables/i18n/Vietnamese.json"
        },
        "order": [[2, "desc"]],
        "columnDefs": [
            { "orderable": false, "targets": [1, 5] } // Không sắp xếp cột Trạng thái, Hành động
        ]
    });

    // Xử lý thay đổi trạng thái
    $('.status-select').change(function() {
        const taskId = $(this).data('task-id');
        const newStatus = $(this).val();
        const $select = $(this);

        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn thay đổi trạng thái?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#007bff',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Lưu',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/projects/tasks/update-assignment-status/',
                    method: 'POST',
                    data: {
                        'task_id': taskId,
                        'status': newStatus,
                        'csrfmiddlewaretoken': getCookie('csrftoken')
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Thành công',
                                text: 'Cập nhật trạng thái thành công!',
                                confirmButtonColor: '#007bff',
                                timer: 3000
                            });
                            $select.data('original-status', newStatus);
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error,
                                confirmButtonColor: '#007bff'
                            });
                            $select.val($select.data('original-status')); // Khôi phục trạng thái
                        }
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: xhr.status === 403 ? 'Không có quyền thực hiện hành động này' : 'Có lỗi xảy ra, vui lòng thử lại!',
                            confirmButtonColor: '#007bff'
                        });
                        $select.val($select.data('original-status')); // Khôi phục trạng thái
                    }
                });
            } else {
                $select.val($select.data('original-status')); // Khôi phục trạng thái
            }
        });
    });

    // Xử lý chỉnh sửa time entry
    $('.edit-entry').click(function() {
        const $row = $(this).closest('tr');
        $row.find('.editable').each(function() {
            const $span = $(this);
            const $input = $span.siblings('input');
            $span.addClass('d-none');
            $input.removeClass('d-none');
        });
        $row.find('.edit-entry').addClass('d-none');
        $row.find('.save-entry, .cancel-entry').removeClass('d-none');
    });

    $('.cancel-entry').click(function() {
        const $row = $(this).closest('tr');
        $row.find('.editable').each(function() {
            const $span = $(this);
            const $input = $span.siblings('input');
            $span.removeClass('d-none');
            $input.addClass('d-none');
        });
        $row.find('.edit-entry').removeClass('d-none');
        $row.find('.save-entry, .cancel-entry').addClass('d-none');
    });

    $('.save-entry').click(function() {
        const $row = $(this).closest('tr');
        const entryId = $row.data('entry-id');
        const startTime = $row.find('input[name="start_time"]').val();
        const endTime = $row.find('input[name="end_time"]').val();

        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn lưu thay đổi?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#007bff',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Lưu',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/projects/time-entries/update/',
                    method: 'POST',
                    data: {
                        'entry_id': entryId,
                        'start_time': startTime,
                        'end_time': endTime,
                        'csrfmiddlewaretoken': getCookie('csrftoken')
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Thành công',
                                text: response.message,
                                confirmButtonColor: '#007bff',
                                timer: 3000
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error,
                                confirmButtonColor: '#007bff'
                            });
                        }
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: xhr.status === 403 ? 'Không có quyền thực hiện hành động này' : 'Có lỗi xảy ra, vui lòng thử lại!',
                            confirmButtonColor: '#007bff'
                        });
                    }
                });
            }
        });
    });

    function createProductivityTimelineChart() {
        console.log('Creating productivity timeline chart with data:', timeByDayData);
    
        // Kiểm tra nếu không có dữ liệu
        if (!timeByDayData || !Array.isArray(timeByDayData) || timeByDayData.length === 0) {
            console.warn('Không có dữ liệu thời gian theo ngày, bỏ qua việc tạo biểu đồ 1');
            const canvas = document.getElementById('timeByDayChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Không có dữ liệu để hiển thị biểu đồ</p></div>';
            }
            return;
        }
    
        // Chuẩn bị dữ liệu
        const days = [];
        const actualHours = [];
        const workEfficiency = [];
        const targetLine = [];
    
        // Sắp xếp ngày tăng dần
        let sortedData = [];
        try {
            sortedData = [...timeByDayData].sort((a, b) => {
                if (!a || !b || !a.day || !b.day) return 0;
                const dateA = new Date(a.day.split('/').reverse().join('-'));
                const dateB = new Date(b.day.split('/').reverse().join('-'));
                return dateA - dateB;
            });
        } catch (e) {
            console.error('Lỗi khi sắp xếp dữ liệu:', e);
            sortedData = timeByDayData;
        }
    
        // Xử lý dữ liệu
        sortedData.forEach(item => {
            if (item && item.day && item.total_time !== undefined && item.total_time !== null) {
                days.push(item.day);
                const totalTime = parseFloat(item.total_time) || 0;
                actualHours.push(totalTime);
                const efficiency = Math.min((totalTime / 8) * 100, 130);
                workEfficiency.push(efficiency);
                targetLine.push(100);
            }
        });
    
        // Kiểm tra xem có đủ dữ liệu để tạo biểu đồ không
        if (days.length === 0 || actualHours.length === 0) {
            console.warn('Không có ngày hoặc dữ liệu hợp lệ trong timeByDayData');
            const canvas = document.getElementById('timeByDayChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Không có dữ liệu hợp lệ để hiển thị biểu đồ</p></div>';
            }
            return;
        }
    
        // Tính trung bình động cho đường xu hướng, thay null bằng 0
        const trendLine = calculateMovingAverage(workEfficiency, 3).map(val => val === null ? 0 : val);
    
        // Tạo biểu đồ
        const ctx = document.getElementById('timeByDayChart').getContext('2d');
        try {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: days,
                    datasets: [
                        {
                            label: 'Thời gian làm việc (giờ)',
                            data: actualHours,
                            backgroundColor: 'rgba(65, 105, 225, 0.7)',
                            borderColor: 'rgba(65, 105, 225, 1)',
                            borderWidth: 1,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Hiệu suất (%)',
                            data: workEfficiency,
                            type: 'line',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.1)',
                            borderWidth: 2,
                            pointRadius: 4,
                            pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                            fill: false,
                            tension: 0.2,
                            yAxisID: 'y1'
                        },
                        {
                            label: 'Xu hướng hiệu suất',
                            data: trendLine,
                            type: 'line',
                            borderColor: 'rgba(255, 159, 64, 1)',
                            borderWidth: 2,
                            pointRadius: 0,
                            borderDash: [5, 5],
                            fill: false,
                            yAxisID: 'y1'
                        },
                        {
                            label: 'Mục tiêu',
                            data: targetLine,
                            type: 'line',
                            borderColor: 'rgba(75, 192, 192, 0.7)',
                            borderWidth: 2,
                            pointRadius: 0,
                            borderDash: [2, 2],
                            fill: false,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Hiệu suất làm việc theo thời gian',
                            font: { size: 16, weight: 'bold' }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    let value = context.raw !== undefined ? context.raw : 0;
                                    if (label.includes('Thời gian')) {
                                        return `${label}: ${value.toFixed(2)} giờ`;
                                    } else if (label.includes('Hiệu suất') || label.includes('Xu hướng')) {
                                        return `${label}: ${value.toFixed(1)}%`;
                                    } else if (label.includes('Mục tiêu')) {
                                        return `${label}: 100%`;
                                    }
                                    return `${label}: ${value}`;
                                }
                            }
                        },
                        legend: {
                            position: 'top',
                            labels: { usePointStyle: true, padding: 15 }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(0, 0, 0, 0.05)' },
                            ticks: { maxRotation: 45, minRotation: 45 }
                        },
                        y: {
                            beginAtZero: true,
                            position: 'left',
                            title: { display: true, text: 'Thời gian (giờ)', font: { weight: 'bold' } },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        y1: {
                            beginAtZero: true,
                            position: 'right',
                            max: 130,
                            title: { display: true, text: 'Hiệu suất (%)', font: { weight: 'bold' } },
                            grid: { display: false }
                        }
                    },
                    interaction: {
                        mode: 'index',
                        intersect: false
                    }
                }
            });
        } catch (error) {
            console.error('Lỗi khi tạo biểu đồ 1:', error);
            const canvas = document.getElementById('timeByDayChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Lỗi khi tạo biểu đồ</p></div>';
            }
        }
    }

    // Hàm tính trung bình động
    function calculateMovingAverage(data, windowSize) {
        if (!Array.isArray(data) || data.length === 0) return [];
        
        const result = [];
        
        // Thêm giá trị null cho những ngày đầu tiên không đủ cửa sổ
        for (let i = 0; i < windowSize - 1; i++) {
            result.push(null);
        }
        
        // Tính trung bình động
        for (let i = windowSize - 1; i < data.length; i++) {
            let sum = 0;
            let validValues = 0;
            for (let j = 0; j < windowSize; j++) {
                if (data[i - j] !== undefined && data[i - j] !== null) {
                    sum += data[i - j];
                    validValues++;
                }
            }
            result.push(validValues > 0 ? sum / validValues : null);
        }
        
        return result;
    }

    function createTaskTimeEfficiencyChart() {
        console.log('Creating task time efficiency chart with data:', timeByTaskData);
    
        // Kiểm tra nếu không có dữ liệu
        if (!timeByTaskData || !Array.isArray(timeByTaskData) || timeByTaskData.length === 0) {
            console.warn('Không có dữ liệu thời gian theo task, bỏ qua việc tạo biểu đồ 2');
            const canvas = document.getElementById('timeByTaskChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Không có dữ liệu để hiển thị biểu đồ</p></div>';
            }
            return;
        }
    
        // Chuẩn bị dữ liệu
        const taskNames = [];
        const estimatedTimes = [];
        const actualTimes = [];
        const efficiencyScores = [];
        const backgrounds = [];
    
        // Lọc nhiệm vụ có ước tính thời gian
        const validTasks = timeByTaskData.filter(task =>
            task &&
            task.task_title &&
            task.estimated_time !== undefined &&
            task.estimated_time !== null &&
            parseFloat(task.estimated_time) > 0 &&
            task.total_time !== undefined &&
            task.total_time !== null &&
            parseFloat(task.total_time) > 0
        );
    
        if (validTasks.length === 0) {
            console.warn('Không có nhiệm vụ nào có dữ liệu ước tính thời gian hợp lệ');
            const canvas = document.getElementById('timeByTaskChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Không có dữ liệu ước tính thời gian để hiển thị biểu đồ</p></div>';
            }
            return;
        }
    
        // Xử lý dữ liệu nhiệm vụ
        validTasks.forEach(task => {
            try {
                let taskName = task.task_title || '';
                if (taskName.length > 20) {
                    taskName = taskName.substring(0, 17) + '...';
                }
                taskNames.push(taskName);
    
                const estimatedTime = parseFloat(task.estimated_time) || 0;
                const actualTime = parseFloat(task.total_time) || 0;
    
                estimatedTimes.push(estimatedTime);
                actualTimes.push(actualTime);
    
                let efficiency = actualTime > 0 ? (estimatedTime / actualTime) * 100 : 0;
                efficiency = Math.min(efficiency, 150);
                efficiencyScores.push(efficiency);
    
                if (efficiency >= 100) {
                    backgrounds.push('rgba(40, 167, 69, 0.8)'); // Xanh lá
                } else if (efficiency >= 75) {
                    backgrounds.push('rgba(255, 193, 7, 0.8)'); // Vàng
                } else {
                    backgrounds.push('rgba(220, 53, 69, 0.8)'); // Đỏ
                }
            } catch (e) {
                console.error('Lỗi khi xử lý task:', task, e);
            }
        });
    
        // Sắp xếp dữ liệu theo hiệu quả
        const sortedIndices = efficiencyScores
            .map((score, index) => ({ score, index }))
            .sort((a, b) => b.score - a.score)
            .map(item => item.index);
    
        const sortedTaskNames = sortedIndices.map(i => taskNames[i]);
        const sortedEstimatedTimes = sortedIndices.map(i => estimatedTimes[i]);
        const sortedActualTimes = sortedIndices.map(i => actualTimes[i]);
        const sortedEfficiencyScores = sortedIndices.map(i => efficiencyScores[i]);
        const sortedBackgrounds = sortedIndices.map(i => backgrounds[i]);
    
        // Tạo biểu đồ
        const ctx = document.getElementById('timeByTaskChart').getContext('2d');
        try {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sortedTaskNames,
                    datasets: [
                        {
                            label: 'Thời gian ước tính (giờ)',
                            data: sortedEstimatedTimes,
                            backgroundColor: 'rgba(54, 162, 235, 0.7)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            order: 2
                        },
                        {
                            label: 'Thời gian thực tế (giờ)',
                            data: sortedActualTimes,
                            backgroundColor: 'rgba(153, 102, 255, 0.7)',
                            borderColor: 'rgba(153, 102, 255, 1)',
                            borderWidth: 1,
                            order: 3
                        },
                        {
                            label: 'Hiệu quả (%)',
                            data: sortedEfficiencyScores,
                            type: 'line',
                            backgroundColor: sortedBackgrounds,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 2,
                            pointRadius: 6,
                            pointHoverRadius: 8,
                            fill: false,
                            yAxisID: 'y1',
                            order: 1
                        }
                    ]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Hiệu quả sử dụng thời gian theo công việc',
                            font: { size: 16, weight: 'bold' }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    let value = context.raw !== undefined ? context.raw : 0;
                                    if (label.includes('Hiệu quả')) {
                                        let rating = value >= 100 ? ' (Xuất sắc)' : value >= 75 ? ' (Tốt)' : ' (Cần cải thiện)';
                                        return `${label}: ${value.toFixed(1)}%${rating}`;
                                    }
                                    return `${label}: ${value.toFixed(2)} giờ`;
                                },
                                footer: function(tooltipItems) {
                                    const index = tooltipItems[0].dataIndex;
                                    const estimated = sortedEstimatedTimes[index];
                                    const actual = sortedActualTimes[index];
                                    const diff = estimated - actual;
                                    return diff >= 0 ? `Tiết kiệm: ${Math.abs(diff).toFixed(2)} giờ` : `Vượt quá: ${Math.abs(diff).toFixed(2)} giờ`;
                                }
                            }
                        },
                        legend: {
                            position: 'top',
                            labels: { usePointStyle: true, padding: 15 }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            title: { display: true, text: 'Thời gian (giờ)', font: { weight: 'bold' } },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        y: {
                            grid: { display: false }
                        },
                        y1: {
                            position: 'right',
                            beginAtZero: true,
                            max: 150,
                            title: { display: true, text: 'Hiệu quả (%)', font: { weight: 'bold' } },
                            grid: { display: false }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Lỗi khi tạo biểu đồ 2:', error);
            const canvas = document.getElementById('timeByTaskChart');
            if (canvas) {
                const container = canvas.parentElement;
                container.innerHTML = '<div class="text-center py-5"><i class="bi bi-exclamation-circle text-muted fs-3"></i><p class="mt-2">Lỗi khi tạo biểu đồ</p></div>';
            }
        }
    }

    // Gọi hàm tạo biểu đồ có kiểm tra
    try {
        // Kiểm tra dữ liệu toàn cầu
        if (typeof timeByDayData === 'undefined') {
            console.error('Biến timeByDayData không được định nghĩa');
            timeByDayData = [];
        }
        
        if (typeof timeByTaskData === 'undefined') {
            console.error('Biến timeByTaskData không được định nghĩa');
            timeByTaskData = [];
        }
        
        console.log('Dữ liệu biểu đồ:', {
            timeByDayData: timeByDayData || [], 
            timeByTaskData: timeByTaskData || []
        });
        
        // Tạo biểu đồ 1 nếu có canvas
        if (document.getElementById('timeByDayChart')) {
            setTimeout(() => {
                try {
                    createProductivityTimelineChart();
                } catch (e) {
                    console.error('Lỗi khi tạo biểu đồ 1:', e);
                }
            }, 100);
        }
        
        // Tạo biểu đồ 2 nếu có canvas
        if (document.getElementById('timeByTaskChart')) {
            setTimeout(() => {
                try {
                    createTaskTimeEfficiencyChart();
                } catch (e) {
                    console.error('Lỗi khi tạo biểu đồ 2:', e);
                }
            }, 200);
        }
    } catch (error) {
        console.error('Lỗi khi tạo biểu đồ:', error);
    }

    // Xuất PDF - Cập nhật chức năng để sử dụng báo cáo mới
    $('#export-pdf').click(function() {
        Swal.fire({
            title: 'Xuất báo cáo',
            text: 'Bạn muốn xuất báo cáo theo định dạng nào?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#007bff',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Báo cáo tháng',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/users/report/?period=monthly';
            }
        });
    });
});

// Hàm chờ canvas sẵn sàng
function waitForCanvas(canvasId, callback) {
    const canvas = document.getElementById(canvasId);
    if (canvas) {
        callback();
        return;
    }
    const observer = new MutationObserver((mutations, obs) => {
        const canvas = document.getElementById(canvasId);
        if (canvas) {
            callback();
            obs.disconnect();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}

// Kiểm tra dữ liệu toàn cầu
if (typeof timeByDayData === 'undefined') {
    console.error('Biến timeByDayData không được định nghĩa');
    timeByDayData = [];
}
if (typeof timeByTaskData === 'undefined') {
    console.error('Biến timeByTaskData không được định nghĩa');
    timeByTaskData = [];
}

console.log('Dữ liệu biểu đồ:', {
    timeByDayData: timeByDayData || [],
    timeByTaskData: timeByTaskData || []
});

// Tạo biểu đồ 1
waitForCanvas('timeByDayChart', () => {
    try {
        createProductivityTimelineChart();
    } catch (e) {
        console.error('Lỗi khi tạo biểu đồ 1:', e);
    }
});

// Tạo biểu đồ 2
waitForCanvas('timeByTaskChart', () => {
    try {
        createTaskTimeEfficiencyChart();
    } catch (e) {
        console.error('Lỗi khi tạo biểu đồ 2:', e);
    }
});