$(document).ready(function() {
    // Xử lý form cập nhật task
    $('#taskUpdateForm').submit(function(e) {
        e.preventDefault();
        var taskId = $(this).data('task-id');
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
        var formData = $(this).serialize() + '&task_id=' + taskId;
        $.ajax({
            url: $(this).data('update-url'),
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Cập nhật task thành công!',
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
                        text: response.error || 'Có lỗi xảy ra!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr) {
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

    // Xử lý form yêu cầu gia hạn
    $('#extensionRequestForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).data('extension-url'),
            type: 'POST',
            data: {
                task_id: $('#taskUpdateForm').data('task-id'),
                requested_deadline: $('#requestDeadline').val(),
                reason: $('#requestReason').val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Yêu cầu gia hạn đã được gửi!',
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(() => {
                        $('#requestDeadline').val('');
                        $('#requestReason').val('');
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
            error: function(xhr) {
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

    // Kích hoạt tooltip
    $('[data-bs-toggle="tooltip"]').tooltip();
});