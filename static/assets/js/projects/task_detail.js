$(document).ready(function() {
    // Lấy CSRF token
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

    // Toggle edit mode
    $('#editTaskBtn').click(function() {
        $('#taskInfoView').addClass('d-none');
        $('#taskUpdateForm').removeClass('d-none');
        $(this).addClass('d-none');
    });

    $('#cancelEditBtn').click(function() {
        $('#taskInfoView').removeClass('d-none');
        $('#taskUpdateForm').addClass('d-none');
        $('#editTaskBtn').removeClass('d-none');
    });

    // Xử lý form cập nhật task
    $('#taskUpdateForm').submit(function(e) {
        e.preventDefault();
        const taskId = $(this).data('task-id');
        const estimatedTimeUser = $('input[name^="estimated_time_"]').val();
        const githubLink = $('#taskGithubLink').val();
        const statusSelect = $('select[name^="status_"]');
        const status = statusSelect.length ? statusSelect.val() : null;

        // Client-side validation
        if (!taskId || isNaN(taskId)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Task ID không hợp lệ!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

        if (estimatedTimeUser && (isNaN(estimatedTimeUser) || estimatedTimeUser < 0)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Thời gian ước lượng không hợp lệ!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

        if (githubLink && !/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/.test(githubLink)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Link GitHub không hợp lệ!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

        if (statusSelect.length && !status) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng chọn trạng thái!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

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
                const formData = $(this).serialize() + '&task_id=' + taskId;
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
                                confirmButtonColor: '#007bff',
                                timer: 3000
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error || 'Có lỗi xảy ra!',
                                confirmButtonColor: '#007bff'
                            });
                        }
                    },
                    error: function(xhr) {
                        let errorMsg = xhr.status === 403 ? 'Không có quyền thực hiện hành động này!' : 'Có lỗi xảy ra, vui lòng thử lại!';
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: errorMsg,
                            confirmButtonColor: '#007bff'
                        });
                    }
                });
            }
        });
    });

    // Xử lý form yêu cầu gia hạn
    $('#extensionRequestForm').submit(function(e) {
        e.preventDefault();
        const requestedDeadline = $('#requestDeadline').val();
        const reason = $('#requestReason').val().trim();

        if (!requestedDeadline) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng chọn ngày gia hạn!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

        if (!reason) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng nhập lý do gia hạn!',
                confirmButtonColor: '#007bff'
            });
            return;
        }

        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn gửi yêu cầu gia hạn?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#007bff',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Gửi',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: $(this).data('extension-url'),
                    type: 'POST',
                    data: {
                        task_id: $('#taskUpdateForm').data('task-id'),
                        requested_deadline: requestedDeadline,
                        reason: reason,
                        csrfmiddlewaretoken: getCookie('csrftoken')
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Thành công',
                                text: 'Yêu cầu gia hạn đã được gửi!',
                                confirmButtonColor: '#007bff',
                                timer: 3000
                            }).then(() => {
                                $('#requestDeadline').val('');
                                $('#requestReason').val('');
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error || 'Có lỗi xảy ra!',
                                confirmButtonColor: '#007bff'
                            });
                        }
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: xhr.status === 403 ? 'Không có quyền thực hiện hành động này!' : 'Có lỗi xảy ra, vui lòng thử lại!',
                            confirmButtonColor: '#007bff'
                        });
                    }
                });
            }
        });
    });

    // Xử lý bắt đầu task
    $('#startTaskBtn').click(function() {
        const taskId = $(this).data('task-id');
        const url = $(this).data('url');

        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn bắt đầu theo dõi task này?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Bắt đầu',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: {
                        task_id: taskId,
                        action: 'start',
                        csrfmiddlewaretoken: getCookie('csrftoken')
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Đã bắt đầu task',
                                text: 'Thời gian đang được theo dõi.',
                                confirmButtonColor: '#28a745',
                                timer: 2000
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error,
                                confirmButtonColor: '#dc3545'
                            });
                        }
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: 'Có lỗi xảy ra khi bắt đầu task.',
                            confirmButtonColor: '#dc3545'
                        });
                    }
                });
            }
        });
    });

    // Xử lý dừng task
    $('#stopTaskBtn').click(function() {
        const taskId = $(this).data('task-id');
        const url = $(this).data('url');

        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn dừng theo dõi task này?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#ffc107',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Dừng',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: {
                        task_id: taskId,
                        action: 'stop',
                        csrfmiddlewaretoken: getCookie('csrftoken')
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Đã dừng task',
                                text: `Thời gian đã được ghi nhận: ${response.duration.toFixed(2)} giờ`,
                                confirmButtonColor: '#28a745',
                                timer: 2000
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Lỗi',
                                text: response.error,
                                confirmButtonColor: '#dc3545'
                            });
                        }
                    },
                    error: function(xhr) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: 'Có lỗi xảy ra khi dừng task.',
                            confirmButtonColor: '#dc3545'
                        });
                    }
                });
            }
        });
    });

    // Khởi tạo tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
});