/**
 * Project Dashboard JavaScript
 * Quản lý tổng quan dự án, biểu đồ và số liệu thống kê
 */

$(document).ready(function() {
  // Khởi tạo các biểu đồ khi trang đã tải xong
  initCharts();

  // Khởi tạo tooltip và popover
  initTooltips();

  // Thêm sự kiện lọc dự án
  setupProjectFilters();

  // Khởi tạo bảng dự án
  initProjectTable();

  // Thêm sự kiện cho timeline
  setupTimelineEvents();
});

/**
 * Khởi tạo các biểu đồ trong dashboard
 */
function initCharts() {
  // Biểu đồ phân bổ dự án theo trạng thái
  initProjectStatusChart();

  // Biểu đồ tiến độ hoàn thành dự án theo thời gian
  initProjectProgressChart();

  // Biểu đồ phân bổ công việc trong dự án
  initTaskDistributionChart();
}

/**
 * Khởi tạo biểu đồ phân bổ dự án theo trạng thái
 */
function initProjectStatusChart() {
  if ($('#projectStatusChart').length > 0) {
    // Lấy dữ liệu từ data-chart attribute nếu có
    var chartData = $('#projectStatusChart').data('chart');

    // Nếu không có dữ liệu, sử dụng dữ liệu mẫu
    if (!chartData) {
      chartData = {
        labels: ['Đang thực hiện', 'Hoàn thành', 'Trễ hạn', 'Đang tạm dừng'],
        datasets: [{
          data: [12, 8, 3, 2],
          backgroundColor: ['#007bff', '#28a745', '#dc3545', '#6c757d'],
          borderWidth: 0
        }]
      };
    }

    var ctx = document.getElementById('projectStatusChart').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 20,
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value / total) * 100);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      }
    });
  }
}

/**
 * Khởi tạo biểu đồ tiến độ hoàn thành dự án theo thời gian
 */
function initProjectProgressChart() {
  if ($('#projectProgressChart').length > 0) {
    // Lấy dữ liệu từ data-chart attribute nếu có
    var chartData = $('#projectProgressChart').data('chart');

    // Nếu không có dữ liệu, sử dụng dữ liệu mẫu
    if (!chartData) {
      chartData = {
        labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'],
        datasets: [{
          label: 'Tiến độ dự án (%)',
          data: [10, 25, 45, 60, 75, 85],
          fill: true,
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          borderColor: '#007bff',
          tension: 0.4
        }]
      };
    }

    var ctx = document.getElementById('projectProgressChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.dataset.label + ': ' + context.raw + '%';
              }
            }
          }
        }
      }
    });
  }
}

/**
 * Khởi tạo biểu đồ phân bổ công việc trong dự án
 */
function initTaskDistributionChart() {
  if ($('#taskDistributionChart').length > 0) {
    // Lấy dữ liệu từ data-chart attribute nếu có
    var chartData = $('#taskDistributionChart').data('chart');

    // Nếu không có dữ liệu, sử dụng dữ liệu mẫu
    if (!chartData) {
      chartData = {
        labels: ['Phát triển', 'Thiết kế', 'Kiểm thử', 'Tài liệu', 'Khác'],
        datasets: [{
          data: [45, 20, 15, 10, 10],
          backgroundColor: ['#007bff', '#28a745', '#ffc107', '#17a2b8', '#6c757d'],
          borderWidth: 0
        }]
      };
    }

    var ctx = document.getElementById('taskDistributionChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0
            }
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    });
  }
}

/**
 * Khởi tạo tooltips cho các thành phần trên dashboard
 */
function initTooltips() {
  // Khởi tạo tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Khởi tạo popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
}

/**
 * Thiết lập bộ lọc dự án
 */
function setupProjectFilters() {
  // Lọc dự án theo trạng thái
  $('.filter-button').on('click', function() {
    var filter = $(this).data('filter');

    // Thêm lớp active cho nút được chọn
    $('.filter-button').removeClass('active');
    $(this).addClass('active');

    if (filter === 'all') {
      // Hiển thị tất cả dự án
      $('.project-item').show();
    } else {
      // Ẩn tất cả dự án
      $('.project-item').hide();
      // Hiển thị dự án phù hợp với bộ lọc
      $('.project-item[data-status="' + filter + '"]').show();
    }
  });

  // Tìm kiếm dự án
  $('#projectSearch').on('keyup', function() {
    var searchTerm = $(this).val().toLowerCase();

    $('.project-item').each(function() {
      var projectName = $(this).find('.project-name').text().toLowerCase();
      var projectDesc = $(this).find('.project-description').text().toLowerCase();

      if (projectName.indexOf(searchTerm) > -1 || projectDesc.indexOf(searchTerm) > -1) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
}

/**
 * Khởi tạo bảng dự án với tính năng sắp xếp và phân trang
 */
function initProjectTable() {
  if ($('#projectsTable').length > 0) {
    $('#projectsTable').DataTable({
      "language": {
        "url": "/static/assets/js/plugin/datatables/i18n/Vietnamese.json"
      },
      "order": [[3, "desc"]], // Sắp xếp theo tiến độ giảm dần
      "pageLength": 5,
      "lengthMenu": [5, 10, 25, 50],
      "responsive": true
    });
  }
}

/**
 * Thiết lập sự kiện cho timeline
 */
function setupTimelineEvents() {
  // Hiển thị chi tiết khi click vào timeline item
  $('.timeline-item').on('click', function() {
    var timelineId = $(this).data('id');

    // Hiển thị modal chi tiết nếu có
    if ($('#timelineModal-' + timelineId).length > 0) {
      var timelineModal = new bootstrap.Modal(document.getElementById('timelineModal-' + timelineId));
      timelineModal.show();
    }
  });
}

/**
 * Chuyển đến trang chi tiết dự án
 * @param {number} projectId - ID của dự án
 */
function viewProjectDetails(projectId) {
  window.location.href = '/projects/detail/' + projectId + '/';
}

/**
 * Tải và cập nhật dữ liệu dự án từ server
 * @param {number} projectId - ID của dự án (nếu có)
 */
function loadProjectData(projectId) {
  var url = '/projects/dashboard-data/';

  if (projectId) {
    url += '?project_id=' + projectId;
  }

  $.ajax({
    url: url,
    method: 'GET',
    dataType: 'json',
    success: function(response) {
      // Cập nhật các thống kê
      updateProjectStats(response.stats);

      // Cập nhật biểu đồ
      updateCharts(response.charts);

      // Cập nhật timeline
      if (response.timeline) {
        updateTimeline(response.timeline);
      }
    },
    error: function(xhr, status, error) {
      console.error('Lỗi khi tải dữ liệu dự án:', error);
      // Hiển thị thông báo lỗi
      showErrorNotification('Không thể tải dữ liệu dự án. Vui lòng thử lại sau.');
    }
  });
}

/**
 * Cập nhật thống kê dự án
 * @param {Object} stats - Dữ liệu thống kê
 */
function updateProjectStats(stats) {
  // Cập nhật số lượng dự án
  $('#totalProjects').text(stats.total_projects || 0);

  // Cập nhật số lượng dự án đang thực hiện
  $('#activeProjects').text(stats.active_projects || 0);

  // Cập nhật số lượng dự án hoàn thành
  $('#completedProjects').text(stats.completed_projects || 0);

  // Cập nhật số lượng dự án trễ hạn
  $('#overdueProjects').text(stats.overdue_projects || 0);
}

/**
 * Cập nhật các biểu đồ
 * @param {Object} charts - Dữ liệu biểu đồ
 */
function updateCharts(charts) {
  // Cập nhật biểu đồ trạng thái dự án
  if (charts.status_chart && window.projectStatusChart) {
    window.projectStatusChart.data = charts.status_chart;
    window.projectStatusChart.update();
  }

  // Cập nhật biểu đồ tiến độ dự án
  if (charts.progress_chart && window.projectProgressChart) {
    window.projectProgressChart.data = charts.progress_chart;
    window.projectProgressChart.update();
  }

  // Cập nhật biểu đồ phân bổ công việc
  if (charts.task_chart && window.taskDistributionChart) {
    window.taskDistributionChart.data = charts.task_chart;
    window.taskDistributionChart.update();
  }
}

/**
 * Cập nhật timeline
 * @param {Array} timelineItems - Danh sách các mục timeline
 */
function updateTimeline(timelineItems) {
  var timelineContainer = $('.timeline');

  // Xóa các mục cũ
  timelineContainer.empty();

  // Thêm các mục mới
  timelineItems.forEach(function(item) {
    var timelineItem = `
      <div class="timeline-item" data-id="${item.id}">
        <div class="timeline-badge"></div>
        <div class="timeline-content">
          <div class="timeline-date">${item.date}</div>
          <h5 class="timeline-title">${item.title}</h5>
          <p class="timeline-text">${item.description}</p>
        </div>
      </div>
    `;

    timelineContainer.append(timelineItem);
  });

  // Cập nhật sự kiện cho timeline
  setupTimelineEvents();
}

/**
 * Hiển thị thông báo lỗi
 * @param {string} message - Nội dung thông báo
 */
function showErrorNotification(message) {
  // Kiểm tra xem có thư viện notifications không
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      icon: 'error',
      title: 'Lỗi',
      text: message,
      confirmButtonText: 'Đóng'
    });
  } else {
    alert(message);
  }
}

// Sự kiện khi tab thay đổi
$('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
  // Lấy ID của tab hiện tại
  var tabId = $(e.target).attr('href');

  // Khởi tạo lại biểu đồ cho tab hiện tại (nếu có)
  if (tabId === '#overview-tab') {
    initProjectStatusChart();
  } else if (tabId === '#progress-tab') {
    initProjectProgressChart();
  } else if (tabId === '#tasks-tab') {
    initTaskDistributionChart();
  }
});
