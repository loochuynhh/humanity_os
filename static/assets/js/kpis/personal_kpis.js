$(document).ready(function() {
    // Handle filter form submission
    $('form').submit(function(e) {
        e.preventDefault();
        const formData = $(this).serialize();
        const url = $(this).data('url');
        if (!url) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Không tìm thấy URL lọc!',
            });
            return;
        }
        window.location.href = `${url}?${formData}`;
    });

    // Handle update KPI
    $('.update-kpi-btn').click(function() {
        const row = $(this).closest('tr');
        const kpiId = row.data('kpi-id');
        const actualValue = row.find('.actual-value-input').val();
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        if (!actualValue || isNaN(actualValue) || actualValue < 0) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng nhập giá trị thực tế hợp lệ!',
            });
            return;
        }

        $.ajax({
            url: '/kpis/update/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {
                kpi_id: kpiId,
                actual_value: actualValue
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Thành công',
                        text: 'Cập nhật KPI thành công!',
                        timer: 2000,
                        timerProgressBar: true
                    });
                    // Cập nhật giao diện
                    row.find('.actual-value-input').prop('disabled', true);
                    row.find('.update-kpi-btn').remove();
                    row.find('.badge').text(response.evaluation).removeClass().addClass('badge').addClass(
                        response.evaluation === 'Exceeded' ? 'bg-success' :
                        response.evaluation === 'Achieved' ? 'bg-primary' :
                        response.evaluation === 'Partially Achieved' ? 'bg-warning' : 'bg-danger'
                    );
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Lỗi',
                        text: response.error,
                    });
                }
            },
            error: function() {
                Swal.fire({
                    icon: 'error',
                    title: 'Lỗi kết nối',
                    text: 'Không thể kết nối đến server, vui lòng thử lại!',
                });
            }
        });
    });
});