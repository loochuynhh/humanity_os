$(document).ready(function() {
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

    // Validate and handle task update form
    $('#taskUpdateForm').submit(function(e) {
        e.preventDefault();
        const taskId = $(this).data('task-id');
        const estimatedTimeUser = $('input[name^="estimated_time_"]').val();
        const githubLink = $('#taskGithubLink').val();
        const status = $('#taskStatus').val();
    
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
                text: 'Thời gian ước lượng của bạn không hợp lệ!',
                confirmButtonColor: '#007bff'
            });
            return;
        }
    
        if (githubLink && !isValidUrl(githubLink)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Link GitHub không hợp lệ!',
                confirmButtonColor: '#007bff'
            });
            return;
        }
    
        if (!status) {
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
                                confirmButtonColor: '#007bff'
                            });
                        }
                    },
                    error: function(xhr) {
                        handleAjaxError(xhr);
                    }
                });
            }
        });
    });

    // Validate and handle extension request form
    $('#extensionRequestForm').submit(function(e) {
        e.preventDefault();
        const requestedDeadline = $('#requestDeadline').val();
        const reason = $('#requestReason').val().trim();

        // Client-side validation
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
                        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Thành công',
                                text: 'Yêu cầu gia hạn đã được gửi!',
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
                                confirmButtonColor: '#007bff'
                            });
                        }
                    },
                    error: function(xhr) {
                        handleAjaxError(xhr);
                    }
                });
            }
        });
    });

    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Helper function to validate URL
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    // Helper function to handle AJAX errors
    function handleAjaxError(xhr) {
        let errorMsg = 'Không thể kết nối đến server, vui lòng thử lại!';
        if (xhr.status === 403) {
            errorMsg = 'Phiên đăng nhập hết hạn hoặc lỗi xác thực. Vui lòng đăng nhập lại!';
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: errorMsg,
                confirmButtonColor: '#007bff'
            }).then(() => {
                window.location.href = '/users/login/?next=' + window.location.pathname;
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi kết nối',
                text: errorMsg,
                confirmButtonColor: '#007bff'
            });
        }
    }

    const startTaskBtn = document.getElementById('startTaskBtn');
    if (startTaskBtn) {
        startTaskBtn.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            const url = this.getAttribute('data-url'); // Lấy URL từ data-url
            if (!url) {
                alert('Lỗi: Không tìm thấy URL API!');
                return;
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: `task_id=${taskId}&action=start`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    startTaskBtn.disabled = true;
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Bắt đầu thực hiện task thành công!',
                        confirmButtonColor: '#007bff',
                        timer: 3000,
                        timerProgressBar: true
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: data.error || 'Có lỗi xảy ra!',
                        confirmButtonColor: '#007bff'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi kết nối',
                    text: 'Không thể kết nối đến server, vui lòng thử lại!',
                    confirmButtonColor: '#007bff'
                });
            });
        });
    }
});
