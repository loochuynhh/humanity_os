/**
 * Project Statistics JavaScript
 * Quản lý hiển thị thống kê chi tiết của dự án
 */

$(document).ready(function() {
  // Khởi tạo biểu đồ
  setupCharts();

  // Xử lý sự kiện thay đổi dự án
  $("#projectFilter").on("change", function() {
    const projectId = $(this).val();
    if (projectId) {
      loadProjectStatistics(projectId);
      // Bật các nút khi đã chọn dự án
      $("#exportData, #printStats").prop("disabled", false);
    } else {
      // Ẩn kết quả khi không chọn dự án
      $("#statisticsResults").addClass("d-none");
      $("#noProjectSelected").removeClass("d-none");
      // Tắt các nút khi không chọn dự án
      $("#exportData, #printStats").prop("disabled", true);
    }
  });

  // Xử lý nút xuất Excel
  $("#exportData").on("click", function() {
    exportToExcel();
  });

  // Xử lý nút in báo cáo
  $("#printStats").on("click", function() {
    printReport();
  });
});

/**
 * Tải dữ liệu thống kê dự án từ API
 * @param {string} projectId - ID của dự án cần hiển thị thống kê
 */
function loadProjectStatistics(projectId) {
  $.ajax({
    url: `/projects/statistics/data/?project_id=${projectId}`,
    method: "GET",
    dataType: "json",
    beforeSend: function() {
      // Hiển thị loading
      $("#projectNameTitle").text("Đang tải...");
      $("#projectDescription").text("Đang tải...");
      $("#projectStartDate").text("Đang tải...");
      $("#projectEndDate").text("Đang tải...");
      $("#projectStatus").text("Đang tải...");
      $("#projectTotalTime").text("Đang tải...");

      $("#totalTasks").text("0");
      $("#completedTasks").text("0");
      $("#inProgressTasks").text("0");
      $("#lateTasks").text("0");

      $("#completedTasksBar, #inProgressTasksBar, #lateTasksBar, #notStartedTasksBar").css("width", "0%");

      $("#memberStatsTable").html('<tr><td colspan="6" class="text-center">Đang tải dữ liệu...</td></tr>');
    },
    success: function(response) {
      if (response.success) {
        // Hiển thị kết quả
        $("#statisticsResults").removeClass("d-none");
        $("#noProjectSelected").addClass("d-none");

        // Cập nhật thông tin dự án
        updateProjectInfo(response);

        // Cập nhật thống kê task
        updateTaskStats(response);

        // Cập nhật biểu đồ
        updateCharts(response);

        // Cập nhật bảng thống kê thành viên
        updateMemberStats(response.user_statistics);
      } else {
        // Hiển thị lỗi
        showError("Không thể tải dữ liệu dự án: " + response.error);
      }
    },
    error: function(xhr, status, error) {
      showError("Lỗi khi tải dữ liệu: " + error);
    }
  });
}

/**
 * Cập nhật thông tin chung của dự án
 * @param {Object} data - Dữ liệu dự án từ API
 */
function updateProjectInfo(data) {
  // Cập nhật tiêu đề và thông tin cơ bản
  $("#projectNameTitle").text(data.project_name);
  $("#projectDescription").text(data.project_description || "Không có mô tả");

  // Cập nhật ngày
  $("#projectStartDate").text(data.start_date ? formatDate(data.start_date) : "Chưa thiết lập");
  $("#projectEndDate").text(data.end_date ? formatDate(data.end_date) : "Chưa thiết lập");

  // Cập nhật trạng thái
  const statusClass = getStatusClass(data.status);
  $("#projectStatus")
    .text(data.status)
    .removeClass("bg-info bg-success bg-warning bg-danger")
    .addClass(statusClass);

  // Cập nhật tổng thời gian
  const hours = Math.floor(data.total_time);
  const minutes = Math.round((data.total_time - hours) * 60);
  $("#projectTotalTime").text(`${hours} giờ ${minutes} phút`);
}

/**
 * Cập nhật thống kê công việc
 * @param {Object} data - Dữ liệu dự án từ API
 */
function updateTaskStats(data) {
  // Cập nhật số lượng
  $("#totalTasks").text(data.total_tasks);
  $("#completedTasks").text(data.completed_tasks);
  $("#inProgressTasks").text(data.in_progress_tasks);
  $("#lateTasks").text(data.late_tasks);

  // Tính tỷ lệ phần trăm
  const total = data.total_tasks || 1; // Tránh chia cho 0
  const completedPercent = (data.completed_tasks / total * 100).toFixed(1);
  const inProgressPercent = (data.in_progress_tasks / total * 100).toFixed(1);
  const latePercent = (data.late_tasks / total * 100).toFixed(1);
  const notStartedPercent = 100 - completedPercent - inProgressPercent - latePercent;

  // Cập nhật progress bar
  $("#completedTasksBar").css("width", `${completedPercent}%`);
  $("#inProgressTasksBar").css("width", `${inProgressPercent}%`);
  $("#lateTasksBar").css("width", `${latePercent}%`);
  $("#notStartedTasksBar").css("width", `${notStartedPercent}%`);
}

/**
 * Khởi tạo các biểu đồ
 */
function setupCharts() {
  // Biểu đồ trạng thái công việc
  const taskStatusCtx = document.getElementById('taskStatusChart');
  window.taskStatusChart = new Chart(taskStatusCtx, {
    type: 'doughnut',
    data: {
      labels: ['Đã hoàn thành', 'Đang thực hiện', 'Trễ hạn', 'Chưa bắt đầu'],
      datasets: [{
        data: [0, 0, 0, 0],
        backgroundColor: ['#28a745', '#ffc107', '#dc3545', '#6c757d'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true,
            pointStyle: 'circle'
          }
        }
      }
    }
  });

  // Biểu đồ thời gian làm việc theo thành viên
  const memberTimeCtx = document.getElementById('memberTimeChart');
  window.memberTimeChart = new Chart(memberTimeCtx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: 'Thời gian làm việc (giờ)',
        data: [],
        backgroundColor: '#007bff',
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Thời gian (giờ)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Thành viên'
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

/**
 * Cập nhật các biểu đồ với dữ liệu mới
 * @param {Object} data - Dữ liệu dự án từ API
 */
function updateCharts(data) {
  // Cập nhật biểu đồ trạng thái công việc
  const statusDist = data.task_status_distribution;
  window.taskStatusChart.data.datasets[0].data = [
    statusDist.Completed || 0,
    statusDist['In progress'] || 0,
    statusDist.Late || 0,
    statusDist['Not started'] || 0
  ];
  window.taskStatusChart.update();

  // Cập nhật biểu đồ thời gian làm việc theo thành viên
  const memberNames = data.user_statistics.map(user => user.user_name);
  const memberTimes = data.user_statistics.map(user => user.total_time);

  window.memberTimeChart.data.labels = memberNames;
  window.memberTimeChart.data.datasets[0].data = memberTimes;
  window.memberTimeChart.update();
}

/**
 * Cập nhật bảng thống kê thành viên
 * @param {Array} members - Danh sách thống kê thành viên
 */
function updateMemberStats(members) {
  let tableHtml = '';

  if (members && members.length > 0) {
    members.forEach(member => {
      const completionRate = member.tasks_count > 0
        ? ((member.completed_tasks / member.tasks_count) * 100).toFixed(1)
        : 0;

      tableHtml += `
        <tr>
          <td>${member.user_name}</td>
          <td>${member.role || 'Thành viên'}</td>
          <td>${member.tasks_count}</td>
          <td>${member.completed_tasks}</td>
          <td>
            <div class="progress" style="height: 5px;">
              <div class="progress-bar bg-success" role="progressbar" style="width: ${completionRate}%"></div>
            </div>
            <small class="text-muted">${completionRate}%</small>
          </td>
          <td>${member.total_time.toFixed(1)}</td>
        </tr>
      `;
    });
  } else {
    tableHtml = '<tr><td colspan="6" class="text-center">Không có dữ liệu thành viên</td></tr>';
  }

  $("#memberStatsTable").html(tableHtml);
}

/**
 * Xuất dữ liệu thống kê ra file Excel
 */
function exportToExcel() {
  const projectId = $("#projectFilter").val();
  if (projectId) {
    window.location.href = `/projects/statistics/export/?project_id=${projectId}`;
  }
}

/**
 * In báo cáo thống kê
 */
function printReport() {
  window.print();
}

/**
 * Hiển thị thông báo lỗi
 * @param {string} message - Nội dung lỗi
 */
function showError(message) {
  // Kiểm tra nếu có hiển thị thông báo dưới dạng toast
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

  // Hiển thị thông báo không có dự án
  $("#statisticsResults").addClass("d-none");
  $("#noProjectSelected").removeClass("d-none");
  $("#noProjectSelected .card-body").html(`
    <i class="bi bi-exclamation-triangle-fill fs-1 text-danger mb-3"></i>
    <h4>Lỗi tải dữ liệu</h4>
    <p class="text-muted">${message}</p>
  `);
}

/**
 * Lấy lớp CSS tương ứng với trạng thái dự án
 * @param {string} status - Trạng thái dự án
 * @returns {string} CSS class tương ứng
 */
function getStatusClass(status) {
  switch (status) {
    case 'Completed':
      return 'bg-success';
    case 'In Progress':
      return 'bg-info';
    case 'Late':
    case 'Delayed':
      return 'bg-danger';
    case 'Paused':
      return 'bg-warning';
    default:
      return 'bg-secondary';
  }
}

/**
 * Định dạng ngày tháng
 * @param {string} dateString - Chuỗi ngày tháng theo định dạng ISO
 * @returns {string} Ngày tháng đã định dạng
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}
