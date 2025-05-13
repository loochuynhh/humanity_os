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

    // Biểu đồ mới 1: Phân bổ thời gian theo dự án
    function createProjectTimeDistributionChart() {
        // Xử lý dữ liệu thời gian theo task để nhóm theo dự án
        const projectData = {};
        
        // Giả sử timeByTaskData là mảng các task và thời gian
        timeByTaskData.forEach(item => {
            // Lấy tên dự án từ tiêu đề task (giả sử format: "ProjectName: TaskName")
            const projectName = item.task_title.split(':')[0].trim();
            if (!projectData[projectName]) {
                projectData[projectName] = 0;
            }
            projectData[projectName] += item.total_time;
        });
        
        // Chuyển đổi dữ liệu thành mảng để sử dụng với Chart.js
        const labels = Object.keys(projectData);
        const data = Object.values(projectData);
        
        // Tạo màu ngẫu nhiên cho các dự án
        const backgroundColors = labels.map(() => {
            const r = Math.floor(Math.random() * 255);
            const g = Math.floor(Math.random() * 255);
            const b = Math.floor(Math.random() * 255);
            return `rgba(${r}, ${g}, ${b}, 0.6)`;
        });
        
        const ctxProjectTime = document.getElementById('timeByDayChart').getContext('2d');
        new Chart(ctxProjectTime, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Phân bổ thời gian theo dự án'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value.toFixed(2)} giờ (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Biểu đồ mới 2: Hiệu suất làm việc theo thời gian
    function createProductivityChart() {
        // Xử lý dữ liệu thời gian theo ngày để tính hiệu suất
        // Hiệu suất = (Thời gian làm việc thực tế / Thời gian dự kiến) * 100
        
        // Giả sử dữ liệu theo ngày cung cấp thời gian làm việc thực tế
        const days = timeByDayData.map(item => item.day);
        const actualTime = timeByDayData.map(item => item.total_time);
        
        // Giả lập thời gian dự kiến (8 giờ làm việc mỗi ngày)
        const estimatedTime = actualTime.map(() => 8);
        
        // Tính hiệu suất
        const productivity = actualTime.map((time, index) => 
            Math.min((time / estimatedTime[index]) * 100, 100) // Giới hạn hiệu suất tối đa 100%
        );
        
        const ctxProductivity = document.getElementById('timeByTaskChart').getContext('2d');
        new Chart(ctxProductivity, {
            type: 'line',
            data: {
                labels: days,
                datasets: [
                    {
                        label: 'Thời gian làm việc (giờ)',
                        data: actualTime,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Hiệu suất (%)',
                        data: productivity,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Hiệu suất làm việc theo thời gian'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Thời gian (giờ)'
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        max: 100,
                        title: {
                            display: true,
                            text: 'Hiệu suất (%)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // Gọi hai hàm tạo biểu đồ mới
    createProjectTimeDistributionChart();
    createProductivityChart();

    // Xuất PDF (tạm thời giữ nguyên)
    $('#export-pdf').click(function() {
        Swal.fire({
            icon: 'info',
            title: 'Thông báo',
            text: 'Chức năng xuất PDF đang được phát triển!',
            confirmButtonColor: '#007bff'
        });
    });
});