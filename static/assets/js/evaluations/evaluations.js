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
        if (!responseId || isNaN(responseId)) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'ID đánh giá không hợp lệ',
                confirmButtonColor: '#007bff'
            });
            return;
        }
        $.ajax({
            url: "/evaluations/feedback-detail/",
            method: 'GET',
            data: { 'response_id': responseId },
            success: function(response) {
                if (response.success) {
                    $('#feedbackDetails').html(response.html);
                    $('#feedbackModal').modal('show');
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
                    text: xhr.status === 403 ? 'Không có quyền xem đánh giá này' : 'Có lỗi xảy ra, vui lòng thử lại!',
                    confirmButtonColor: '#007bff'
                });
            }
        });
    });

    // Xử lý mở modal gửi form
    $('.submit-form').click(function() {
        const formId = $(this).closest('tr').data('form-id');
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
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: xhr.status === 403 ? 'Không có quyền truy cập form này' : 'Có lỗi xảy ra, vui lòng thử lại!',
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
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: xhr.status === 403 ? 'Không có quyền truy cập form này' : 'Có lỗi xảy ra, vui lòng thử lại!',
                    confirmButtonColor: '#007bff'
                });
            }
        });
    });
});