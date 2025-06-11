/**
 * Common JavaScript functions for Project Management pages
 */

// Khởi tạo tooltips trên các trang
function initTooltips() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl, {
      boundary: document.body
    });
  });
}

// Hàm định dạng số với dấu phân cách hàng nghìn
function formatNumber(number) {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Hàm định dạng thời gian từ giờ thành chuỗi "Xh Ym"
function formatTime(hours) {
  if (hours === null || hours === undefined) return '0h 0m';
  var h = Math.floor(hours);
  var m = Math.round((hours - h) * 60);
  return h + 'h ' + m + 'm';
}

// Hàm định dạng ngày giờ thành chuỗi "DD/MM/YYYY HH:MM"
function formatDateTime(dateTime) {
  if (!dateTime) return '';
  var date = new Date(dateTime);
  var day = String(date.getDate()).padStart(2, '0');
  var month = String(date.getMonth() + 1).padStart(2, '0');
  var year = date.getFullYear();
  var hours = String(date.getHours()).padStart(2, '0');
  var minutes = String(date.getMinutes()).padStart(2, '0');

  return day + '/' + month + '/' + year + ' ' + hours + ':' + minutes;
}

// Hàm kiểm tra ngày quá hạn
function isOverdue(deadline) {
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var deadlineDate = new Date(deadline);
  deadlineDate.setHours(0, 0, 0, 0);
  return deadlineDate < today;
}

// Hàm tính số ngày còn lại đến deadline
function daysUntilDeadline(deadline) {
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var deadlineDate = new Date(deadline);
  deadlineDate.setHours(0, 0, 0, 0);
  var timeDiff = deadlineDate.getTime() - today.getTime();
  return Math.ceil(timeDiff / (1000 * 3600 * 24));
}

// Hàm tạo class badge dựa vào trạng thái
function getStatusBadgeClass(status) {
  switch (status.toLowerCase()) {
    case 'completed':
    case 'hoàn thành':
      return 'bg-success';
    case 'in progress':
    case 'đang thực hiện':
      return 'bg-primary';
    case 'to-do':
    case 'chưa bắt đầu':
      return 'bg-secondary';
    case 'late':
    case 'trễ hạn':
      return 'bg-danger';
    case 'paused':
    case 'tạm dừng':
      return 'bg-warning';
    default:
      return 'bg-secondary';
  }
}

// Hàm mặc định cho việc tạo DataTables
function createDataTable(tableId, options = {}) {
  const defaultOptions = {
    language: {
      url: "/static/assets/js/plugin/datatables/i18n/Vietnamese.json"
    },
    pageLength: 10,
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "Tất cả"]],
    responsive: true,
    dom: '<"top"fl>rt<"bottom"ip>',
    order: [[0, "asc"]]
  };

  const mergedOptions = Object.assign({}, defaultOptions, options);
  return $(tableId).DataTable(mergedOptions);
}

// Hàm tạo biểu đồ doughnut tiêu chuẩn
function createDoughnutChart(canvasId, data, options = {}) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      }
    }
  };

  const mergedOptions = Object.assign({}, defaultOptions, options);

  return new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: mergedOptions
  });
}

// Hàm tạo biểu đồ line tiêu chuẩn
function createLineChart(canvasId, data, options = {}) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false
  };

  const mergedOptions = Object.assign({}, defaultOptions, options);

  return new Chart(ctx, {
    type: 'line',
    data: data,
    options: mergedOptions
  });
}

// Hàm tạo biểu đồ bar tiêu chuẩn
function createBarChart(canvasId, data, options = {}) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    barThickness: 20
  };

  const mergedOptions = Object.assign({}, defaultOptions, options);

  return new Chart(ctx, {
    type: 'bar',
    data: data,
    options: mergedOptions
  });
}

// Hàm hiển thị thông báo lỗi
function showError(message) {
  alert(message);
}

// Hàm hiển thị thông báo thành công
function showSuccess(message) {
  alert(message);
}

// Khởi tạo tooltips khi document ready
$(document).ready(function() {
  initTooltips();
});
