(function ($) {
  $(document).ready(function () {
      // Xử lý preview ảnh đại diện
      $('#avatarInput').change(function (e) {
          if (this.files && this.files[0]) {
              var reader = new FileReader();
              reader.onload = function (e) {
                  $('#avatar-preview').attr('src', e.target.result);
              };
              reader.readAsDataURL(this.files[0]);
          }
      });

      // Focus nút submit khi mở modal chỉnh sửa
      $('#editProfileModal').on('shown.bs.modal', function () {
          $(this).find('button[type="submit"]').focus();
      });

      // Xử lý form cập nhật hồ sơ
      $('#profileForm').on('submit', function (e) {
          e.preventDefault();

          var $form = $(this);
          var formData = new FormData(this);
          var updateUrl = $form.attr('action');
          var csrfToken = $form.find('input[name="csrfmiddlewaretoken"]').val();

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
                  console.error('AJAX error:', status, error);
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

      // Xử lý form đổi mật khẩu
      $('#changePasswordForm').on('submit', function (e) {
          e.preventDefault();

          var $form = $(this);
          var formData = $form.serialize();
          var updateUrl = $form.attr('action');
          var csrfToken = $form.find('input[name="csrfmiddlewaretoken"]').val();

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
              headers: {
                  'X-CSRFToken': csrfToken
              },
              success: function (response) {
                  if (response.success) {
                      Swal.fire({
                          icon: 'success',
                          title: 'Thành công',
                          text: response.message || 'Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!',
                          confirmButtonText: 'OK',
                          confirmButtonColor: '#007bff',
                          timer: 3000,
                          timerProgressBar: true
                      }).then(() => {
                          window.location.href = '/users/login/';
                      });
                  } else {
                      Swal.fire({
                          icon: 'error',
                          title: 'Lỗi',
                          text: response.message || 'Có lỗi xảy ra khi đổi mật khẩu',
                          confirmButtonText: 'OK',
                          confirmButtonColor: '#007bff'
                      });
                  }
              },
              error: function (xhr, status, error) {
                  console.error('AJAX error:', status, error);
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

      // Xử lý form tải lên ảnh khuôn mặt
      $('#faceImageForm').on('submit', function (e) {
          e.preventDefault();

          var $form = $(this);
          var formData = new FormData(this);
          var uploadUrl = $form.attr('action');
          var csrfToken = $form.find('input[name="csrfmiddlewaretoken"]').val();

          if (!csrfToken || !uploadUrl) {
              console.error('Missing CSRF token or upload URL');
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
              url: uploadUrl,
              type: 'POST',
              data: formData,
              processData: false,
              contentType: false,
              headers: {
                  'X-CSRFToken': csrfToken
              },
              success: function (response) {
                  if (response.success) {
                      Swal.fire({
                          icon: 'success',
                          title: 'Thành công',
                          text: response.message || 'Ảnh khuôn mặt đã được tải lên!',
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
                          text: response.error || 'Có lỗi xảy ra khi tải lên ảnh',
                          confirmButtonText: 'OK',
                          confirmButtonColor: '#007bff'
                      });
                  }
              },
              error: function (xhr, status, error) {
                  console.error('AJAX error:', status, error);
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

      // Thêm hàm hiển thị ảnh check-in/check-out
      function showImage(imageUrl, title) {
          Swal.fire({
              title: title,
              imageUrl: imageUrl,
              imageWidth: 400,
              imageHeight: 300,
              imageAlt: title,
              confirmButtonText: 'Đóng',
              confirmButtonColor: '#007bff'
          });
      }

      // Thêm vào phần document ready
      $(document).ready(function() {
          // Kích hoạt tooltips
          var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
          var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
              return new bootstrap.Tooltip(tooltipTriggerEl);
          });

          // Thêm hàm showImage vào window để có thể gọi từ onclick
          window.showImage = showImage;
      });
  });
})(jQuery);
