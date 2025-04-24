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

    // Vẽ biểu đồ thời gian theo ngày
    const ctxDay = document.getElementById('timeByDayChart').getContext('2d');
    new Chart(ctxDay, {
        type: 'bar',
        data: {
            labels: timeByDayData.map(item => item.day),
            datasets: [{
                label: 'Thời gian làm việc (giờ)',
                data: timeByDayData.map(item => item.total_time),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Giờ'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    // Vẽ biểu đồ phân bổ thời gian theo task
    const ctxTask = document.getElementById('timeByTaskChart').getContext('2d');
    new Chart(ctxTask, {
        type: 'pie',
        data: {
            labels: timeByTaskData.map(item => item.task_title),
            datasets: [{
                data: timeByTaskData.map(item => item.total_time),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                ]
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });

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