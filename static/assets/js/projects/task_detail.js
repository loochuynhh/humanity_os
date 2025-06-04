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

    console.log("Task detail JS đã tải thành công");
    console.log("Bootstrap version:", typeof bootstrap !== 'undefined' ? 'Đã tải' : 'Chưa tải');
    
    // Kiểm tra modal element trong DOM
    const modalElement = document.getElementById('aiTimeEstimationModal');
    console.log("Modal element:", modalElement);
    
    // Lưu trữ tham chiếu đến modal
    let aiTimeEstimationModalElement = modalElement;
    let aiTimeEstimationModal = null;
    
    // Đảm bảo bootstrap đã tải trước khi khởi tạo modal
    function initializeModal() {
        if (!aiTimeEstimationModalElement) {
            console.error('Không tìm thấy phần tử modal với ID "aiTimeEstimationModal"');
            return false;
        }
        
        if (typeof bootstrap === 'undefined') {
            console.error('Bootstrap chưa được tải');
            return false;
        }
        
        try {
            // Thử khởi tạo modal với bootstrap
            aiTimeEstimationModal = new bootstrap.Modal(aiTimeEstimationModalElement);
            console.log('Modal khởi tạo thành công (Bootstrap)');
            return true;
        } catch (error) {
            console.error('Lỗi khởi tạo modal với Bootstrap:', error);
            try {
                // Thử khởi tạo với jQuery nếu Bootstrap thất bại
                console.log('Thử khởi tạo với jQuery...');
                $(aiTimeEstimationModalElement).modal({backdrop: 'static', keyboard: false});
                console.log('Modal khởi tạo thành công (jQuery)');
                // Tạo wrapper function để gọi show/hide dễ dàng
                aiTimeEstimationModal = {
                    show: function() {
                        $(aiTimeEstimationModalElement).modal('show');
                    },
                    hide: function() {
                        $(aiTimeEstimationModalElement).modal('hide');
                    }
                };
                return true;
            } catch (jqError) {
                console.error('Lỗi khởi tạo modal với jQuery:', jqError);
                return false;
            }
        }
    }
    
    // Lưu trữ HTML ban đầu của form để khôi phục sau khi hủy
    const originalFormHtml = $('#taskUpdateForm').html();
    
    // Xử lý sự kiện click vào nút đề xuất thời gian
    $(document).on('click', '.suggest-time-btn', function(e) {
        e.preventDefault();
        console.log('Đã nhấp nút đề xuất thời gian');
        
        // Kiểm tra và khởi tạo modal nếu chưa
        if (!aiTimeEstimationModal) {
            const initialized = initializeModal();
            if (!initialized) {
                console.error("Không thể khởi tạo modal");
                alert('Không thể mở modal đề xuất. Vui lòng tải lại trang.');
                return;
            }
        }
        
        const taskId = $(this).data('task-id');
        const estimatedTimeInput = $(this).closest('.input-group').find('input');
        const userId = estimatedTimeInput.attr('name').replace('estimated_time_', '');
        
        console.log("Task ID:", taskId);
        console.log("User ID:", userId);
        
        // Reset modal state
        $('#aiTimeEstimationContent').addClass('d-none');
        $('#aiTimeEstimationLoading').removeClass('d-none');
        $('#aiTimeEstimationError').addClass('d-none');
        
        // Thử khởi tạo hoặc hiển thị modal với nhiều cách
        try {
            console.log("Đang mở modal...");
            
            // Phương án 1: Sử dụng Bootstrap modal instance
            if (aiTimeEstimationModal && typeof aiTimeEstimationModal.show === 'function') {
                aiTimeEstimationModal.show();
            } 
            // Phương án 2: Sử dụng jQuery modal
            else if ($.fn.modal) {
                $(aiTimeEstimationModalElement).modal('show');
            } 
            // Phương án 3: Hiện modal bằng cách thay đổi class
            else {
                $(aiTimeEstimationModalElement).addClass('show').css('display', 'block');
                $('body').addClass('modal-open').append('<div class="modal-backdrop fade show"></div>');
            }
            
            console.log("Modal đã được mở");
        } catch (modalError) {
            console.error("Lỗi khi mở modal:", modalError);
            alert('Không thể mở modal đề xuất. Vui lòng tải lại trang.');
            return;
        }
        
        // Gọi API để lấy đề xuất thời gian
        $.ajax({
            url: '/projects/api/suggest-time-for-task/',
            type: 'POST',
            data: JSON.stringify({
                task_id: taskId,
                user_id: userId
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                console.log("Nhận phản hồi API thành công:", data);
                
                // Ẩn loading
                $('#aiTimeEstimationLoading').addClass('d-none');
                
                if (data.error) {
                    // Hiển thị lỗi
                    $('#timeErrorMessage').text(data.error);
                    $('#aiTimeEstimationError').removeClass('d-none');
                } else {
                    // Hiển thị kết quả
                    $('#suggestedTime').text(data.suggested_time + ' giờ');
                    $('#timeEstimationReasoning').html(data.reasoning);
                    $('#aiTimeEstimationContent').removeClass('d-none');
                    
                    // Xử lý nút áp dụng
                    $('#applyTimeEstimation').off('click').on('click', function() {
                        estimatedTimeInput.val(data.suggested_time);
                        
                        // Đóng modal
                        if (aiTimeEstimationModal && typeof aiTimeEstimationModal.hide === 'function') {
                            aiTimeEstimationModal.hide();
                        } else if ($.fn.modal) {
                            $(aiTimeEstimationModalElement).modal('hide');
                        } else {
                            $(aiTimeEstimationModalElement).removeClass('show').css('display', 'none');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                        }
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error('Lỗi API:', xhr.responseText);
                // Ẩn loading và hiển thị lỗi
                $('#aiTimeEstimationLoading').addClass('d-none');
                $('#timeErrorMessage').text('Không thể kết nối với máy chủ. Vui lòng thử lại sau.');
                $('#aiTimeEstimationError').removeClass('d-none');
                console.error('Error:', error);
            }
        });
    });

    // Toggle edit mode
    $('#editTaskBtn').click(function() {
        $('#taskInfoView').addClass('d-none');
        $('#taskUpdateForm').removeClass('d-none');
        $(this).addClass('d-none');
    });

    $('#cancelEditBtn').click(function() {
        // Khôi phục HTML ban đầu của form trước khi ẩn nó
        $('#taskUpdateForm').html(originalFormHtml);
        
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

    // Kiểm tra vị trí của modal trong DOM sau khi trang tải xong
    setTimeout(function() {
        console.log("Kiểm tra modal sau 1 giây:");
        const modalCheck = document.getElementById('aiTimeEstimationModal');
        console.log("Modal element tồn tại:", !!modalCheck);
    }, 1000);
});