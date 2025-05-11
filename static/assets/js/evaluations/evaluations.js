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

    // Khởi tạo DataTable
    $('#feedbackTable, #receivedTable, #sentTable, #formTable').DataTable({
        "language": {
            "url": "/static/assets/js/plugin/datatables/i18n/Vietnamese.json"
        },
        "order": [[2, "desc"]],
        "columnDefs": [
            { "orderable": false, "targets": [4] } // Không sắp xếp cột Hành động
        ]
    });

    // Xử lý xem chi tiết đánh giá
    $('.view-feedback').click(function() {
        const responseId = $(this).closest('tr').data('response-id');

        // Hiển thị loading
        Swal.fire({
            title: 'Đang tải...',
            allowOutsideClick: false,
            showConfirmButton: false,
            willOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            url: "/evaluations/feedback-detail/",
            method: 'GET',
            data: { 'response_id': responseId },
            success: function(response) {
                Swal.close();
                if (response.success) {
                    $('#feedbackDetails').html(response.html);
                    $('#feedbackModal').modal('show');
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: response.error || 'Có lỗi xảy ra khi lấy thông tin đánh giá',
                        confirmButtonColor: '#007bff'
                    });
                }
            },
            error: function(xhr) {
                Swal.close();
                let errorMessage = 'Có lỗi xảy ra, vui lòng thử lại!';

                if (xhr.status === 403) {
                    errorMessage = 'Không có quyền xem đánh giá này';
                } else if (xhr.status === 400) {
                    errorMessage = 'Yêu cầu không hợp lệ';

                    // Thử lấy thông báo lỗi chi tiết từ response
                    try {
                        const response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            errorMessage = response.error;
                        }
                    } catch (e) {
                        // Ignore parsing errors
                    }
                }

                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: errorMessage,
                    confirmButtonColor: '#007bff'
                });
            }
        });
    });

    // Xử lý mở modal gửi form
    $('.submit-form').click(function() {
        const formId = $(this).closest('tr').data('form-id');
        const formType = $(this).closest('tr').find('.badge').text().trim().toLowerCase();

        // Kiểm tra nếu là form review mà không phải quản lý
        if (formType === 'review' && !['Manager', 'Admin'].includes(userRole)) {
            Swal.fire({
                icon: 'error',
                title: 'Quyền hạn không đủ',
                text: 'Chỉ quản lý mới có quyền thực hiện đánh giá review',
                confirmButtonColor: '#007bff'
            });
            return false;
        }

        $.ajax({
            url: "/evaluations/submit-form/",
            method: 'GET',
            data: { 'form_id': formId },
            success: function(response) {
                if (response.success) {
                    $('#formContent').html(response.html);
                    $('#submitFormModal').modal('show');
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
                let errorMessage = 'Có lỗi xảy ra, vui lòng thử lại!';

                if (xhr.status === 403) {
                    errorMessage = 'Không có quyền thực hiện đánh giá này';
                }

                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: errorMessage,
                    confirmButtonColor: '#007bff'
                });
            }
        });
    });

    // Xử lý gửi form
    $('#submitForm').click(function() {
        const formData = $('#evaluationForm').serialize();
        Swal.fire({
            title: 'Xác nhận',
            text: 'Bạn có chắc muốn gửi đánh giá này?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#007bff',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Gửi',
            cancelButtonText: 'Hủy'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: "/evaluations/submit-form/",
                    method: 'POST',
                    data: formData,
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Thành công',
                                text: response.message,
                                confirmButtonColor: '#007bff',
                                timer: 3000
                            }).then(() => {
                                $('#submitFormModal').modal('hide');
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
                            text: xhr.status === 403 ? 'Không có quyền gửi đánh giá này' : 'Có lỗi xảy ra, vui lòng thử lại!',
                            confirmButtonColor: '#007bff'
                        });
                    }
                });
            }
        });
    });

    // Xử lý gửi đánh giá mới
    $('.new-evaluation').click(function() {
        const formId = $(this).closest('tr').data('form-id');
        const formType = $(this).closest('tr').find('.badge').text().trim().toLowerCase();

        // Kiểm tra nếu là form review mà không phải quản lý
        if (formType === 'review' && !['Manager', 'Admin'].includes(userRole)) {
            Swal.fire({
                icon: 'error',
                title: 'Quyền hạn không đủ',
                text: 'Chỉ quản lý mới có quyền thực hiện đánh giá review',
                confirmButtonColor: '#007bff'
            });
            return false;
        }

        $.ajax({
            url: "/evaluations/submit-form/",
            method: 'GET',
            data: { 'form_id': formId },
            success: function(response) {
                if (response.success) {
                    $('#formContent').html(response.html);
                    $('#submitFormModal').modal('show');
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
                let errorMessage = 'Có lỗi xảy ra, vui lòng thử lại!';

                if (xhr.status === 403) {
                    errorMessage = 'Không có quyền thực hiện đánh giá này';
                }

                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: errorMessage,
                    confirmButtonColor: '#007bff'
                });
            }
        });
    });
});
