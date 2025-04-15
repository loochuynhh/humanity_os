
(function ($) {
    $(document).ready(function () {
        $('#avatarInput').change(function (e) {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#avatar-preview').attr('src', e.target.result);
                };
                reader.readAsDataURL(this.files[0]);
            }
        });

        $('#editProfileModal').on('shown.bs.modal', function () {
            $(this).find('button[type="submit"]').focus();
        });

        $('#profileForm').on('submit', function (e) {
            e.preventDefault();
            console.log('Form submitted'); // Thêm log để kiểm tra

            var $form = $(this);
            var formData = new FormData(this);
            var updateUrl = $form.attr('action');
            var csrfToken = $form.find('input[name="csrfmiddlewaretoken"]').val();

            console.log('Update URL:', updateUrl); // Log URL
            console.log('CSRF Token:', csrfToken); // Log CSRF token

            if (!csrfToken || !updateUrl) {
                console.error('Missing CSRF token or update URL');
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi',
                    text: 'Không thể gửi yêu cầu. Vui lòng tải lại trang!',
                    confirmButtonText: 'OK',
                    confirmButtonColor: '#007bff'
                });
                return;
            }

            $.ajax({
                url: updateUrl,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    console.log('Server response:', response); 
                    if (response.success) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Thành công',
                            text: 'Hồ sơ đã được cập nhật!',
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
                            text: response.error || 'Có lỗi xảy ra khi cập nhật hồ sơ',
                            confirmButtonText: 'OK',
                            confirmButtonColor: '#007bff'
                        });
                    }
                },
                error: function (xhr, status, error) {
                    console.error('AJAX error:', status, error); // Log lỗi AJAX
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

        $('#print-profile').click(function () {
            window.print();
        });
    });
})(jQuery);