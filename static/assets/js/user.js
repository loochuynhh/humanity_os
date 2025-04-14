$(document).ready(function() {
    // Xử lý upload avatar preview
    $('#avatarInput').change(function(e) {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#avatar-edit-preview').attr('src', e.target.result);
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  
    // Xử lý submit form
    $('#profileForm').submit(function(e) {
      e.preventDefault();
      var formData = new FormData(this);
      
      $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
          'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
          if (response.success) {
            location.reload();
          } else {
            alert(response.error || 'Có lỗi xảy ra khi cập nhật');
          }
        },
        error: function() {
          alert('Lỗi kết nối, vui lòng thử lại');
        }
      });
    });
  
    // In hồ sơ
    $('#print-profile').click(function() {
      window.print();
    });
  });