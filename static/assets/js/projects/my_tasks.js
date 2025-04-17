$(document).ready(function() {
    // Lấy CSRF token từ form
    var $form = $('#taskDetailsForm');
    var csrftoken = $form.find('input[name="csrfmiddlewaretoken"]').val();

    // Khởi tạo DataTables
    var table = $('#tasksTable').DataTable({
        "language": {
            "url": "/static/assets/js/plugin/datatables/i18n/Vietnamese.json"
        },
        "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
               "<'row'<'col-sm-12'tr>>" +
               "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        "columnDefs": [
            { "orderable": false, "targets": [4, 5, 6] } // Không cho phép sắp xếp cột Tổng thời gian, Tiến độ, Hành động
        ],
        "initComplete": function() {
            $('#tasksTable_wrapper').addClass('loaded');
        }
    });

    // Lọc theo dự án
    $('#projectFilter').change(function() {
        table.column(1).search($(this).val()).draw();
    });

    // Lọc theo trạng thái
    $('#statusFilter').change(function() {
        table.column(3).search($(this).val()).draw();
    });

    // Đặt lại bộ lọc
    $('#resetFilter').click(function() {
        $('#projectFilter, #statusFilter').val('').trigger('change');
        table.search('').columns().search('').draw();
    });

    // Cập nhật trạng thái task
    $('.status-update').change(function() {
        var taskId = $(this).data('task-id');
        var status = $(this).val();
        if (!taskId || isNaN(taskId)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Task ID không hợp lệ!',
                confirmButtonText: 'OK',
                confirmButtonColor: '#007bff'
            });
            return;
        }
        $.ajax({
            url: '/projects/tasks/update-status/',
            type: 'POST',
            data: {
                task_id: taskId,
                status: status
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Cập nhật trạng thái thành công!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: response.error || 'Có lỗi xảy ra!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr, status, error) {
                let errorMsg = 'Không thể kết nối đến server, vui lòng thử lại!';
                if (xhr.status === 403) {
                    errorMsg = 'Phiên đăng nhập hết hạn hoặc lỗi xác thực. Vui lòng đăng nhập lại!';
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    }).then(() => {
                        window.location.href = '/users/login/?next=' + window.location.pathname;
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi kết nối',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            }
        });
    });

    // Bật/tắt tracking thời gian
    $('.toggle-time').click(function() {
        var taskId = $(this).data('task-id');
        var action = $(this).text().trim() === 'Bắt đầu' ? 'start' : 'stop';
        if (!taskId || isNaN(taskId)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Task ID không hợp lệ!',
                confirmButtonText: 'OK',
                confirmButtonColor: '#007bff'
            });
            return;
        }
        $.ajax({
            url: '/projects/tasks/toggle-time/',
            type: 'POST',
            data: {
                task_id: taskId,
                action: action
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(data) {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Thao tác tracking thời gian thành công!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: data.error || 'Có lỗi xảy ra!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr, status, error) {
                let errorMsg = 'Không thể kết nối đến server, vui lòng thử lại!';
                if (xhr.status === 403) {
                    errorMsg = 'Phiên đăng nhập hết hạn hoặc lỗi xác thực. Vui lòng đăng nhập lại!';
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    }).then(() => {
                        window.location.href = '/users/login/?next=' + window.location.pathname;
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi kết nối',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            }
        });
    });

    // Xem chi tiết task
    $('.view-details').click(function() {
        var taskId = $(this).data('task-id');
        $('#taskId').val(taskId);
        $('#taskTitle').val($(this).data('title'));
        $('#taskDescription').val($(this).data('description'));
        $('#taskProject').val($(this).data('project'));
        $('#taskDeadline').val($(this).data('deadline'));
        $('#taskStatus').val($(this).data('status'));
        $('#taskDifficulty').val($(this).data('difficulty'));
        $('#taskEstimatedTime').val($(this).data('estimated-time'));
        $('#taskGithubLink').val($(this).data('github-link'));
        $('#taskNotes').val($(this).data('notes'));

        // Load lịch sử thời gian
        var timeEntries = $(this).data('time-entries');
        var entriesHtml = timeEntries > 0 ? '<ul>' : '<p>Chưa có lịch sử thời gian.</p>';
        if (timeEntries > 0) {
            // Dữ liệu thời gian được truyền từ data-time-entries-html
            var entriesData = $(this).data('time-entries-html');
            if (entriesData) {
                entriesHtml += entriesData;
            }
            entriesHtml += '</ul>';
        }
        $('#timeEntries').html(entriesHtml);

        $('#taskModal').modal('show');
    });

    // Lưu chi tiết task
    $('#saveTaskDetails').click(function() {
        $.ajax({
            url: '/projects/tasks/update-details/',
            type: 'POST',
            data: $('#taskDetailsForm').serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: response.message || 'Cập nhật task thành công!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(() => {
                        $('#taskModal').modal('hide');
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: response.error || 'Có lỗi xảy ra!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr, status, error) {
                let errorMsg = 'Không thể kết nối đến server, vui lòng thử lại!';
                if (xhr.status === 403) {
                    errorMsg = 'Phiên đăng nhập hết hạn hoặc lỗi xác thực. Vui lòng đăng nhập lại!';
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    }).then(() => {
                        window.location.href = '/users/login/?next=' + window.location.pathname;
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi kết nối',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            }
        });
    });

    // Gửi yêu cầu gia hạn deadline
    $('#requestExtension').click(function() {
        var requestedDeadline = $('#requestDeadline').val();
        var reason = $('#requestReason').val();
        if (!requestedDeadline || !reason) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng cung cấp ngày gia hạn và lý do!',
                confirmButtonText: 'OK',
                confirmButtonColor: '#007bff'
            });
            return;
        }
        var formData = $('#taskDetailsForm').serialize();
        $.ajax({
            url: '/projects/tasks/request-deadline-extension/',
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: response.message || 'Yêu cầu gia hạn đã được gửi!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(() => {
                        $('#taskModal').modal('hide');
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: response.error || 'Có lỗi xảy ra!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr, status, error) {
                let errorMsg = 'Không thể kết nối đến server, vui lòng thử lại!';
                if (xhr.status === 403) {
                    errorMsg = 'Phiên đăng nhập hết hạn hoặc lỗi xác thực. Vui lòng đăng nhập lại!';
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    }).then(() => {
                        window.location.href = '/users/login/?next=' + window.location.pathname;
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi kết nối',
                        text: errorMsg,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            }
        });
    });
});