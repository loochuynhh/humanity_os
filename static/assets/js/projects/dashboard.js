/**
 * Humanity OS - Project Dashboard JavaScript
 * Quản lý các chức năng tương tác trên dashboard dự án
 */

$(document).ready(function() {
    // Khởi tạo tooltip Bootstrap
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Lấy dữ liệu dashboard từ API
    loadDashboardData();

    // Xử lý sự kiện khi tab thay đổi
    $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        // Vẽ lại biểu đồ khi tab active
        const targetId = $(e.target).attr('href');
        if (targetId === '#time-tab') {
            if (window.timeChart) {
                window.timeChart.resize();
            }
        } else if (targetId === '#projects-tab') {
            if (window.projectsChart) {
                window.projectsChart.resize();
            }
        }
    });

    // Nút làm mới dữ liệu
    $('#refreshDashboard').on('click', function() {
        loadDashboardData();
    });
});

/**
 * Tải dữ liệu dashboard từ API
 */
function loadDashboardData() {
    // Hiển thị loading
    showLoading(true);

    // Gọi API
    $.ajax({
        url: '/projects/api/dashboard-data/',
        method: 'GET',
        success: function(response) {
            // Cập nhật thông tin thống kê
            updateStats(response);

            // Cập nhật dự án gần đây
            updateProjects(response.recent_projects);

            // Cập nhật danh sách task sắp đến hạn
            updateUpcomingTasks(response.upcoming_tasks);

            // Ẩn loading
            showLoading(false);
        },
        error: function(xhr, status, error) {
            console.error('Error loading dashboard data:', error);
            showLoading(false);
            showErrorMessage('Không thể tải dữ liệu dashboard. Vui lòng thử lại sau.');
        }
    });
}

/**
 * Cập nhật các thống kê trên dashboard
 */
function updateStats(data) {
    // Cập nhật số liệu
    $('#totalProjects').text(data.total_projects);
    $('#activeProjects').text(data.active_projects);
    $('#totalTasks').text(data.total_tasks);
    $('#completedTasks').text(data.completed_tasks);

    // Cập nhật tiến độ
    const completionRate = data.completion_rate;
    $('#completionRate').text(completionRate + '%');
    $('#completionProgress').css('width', completionRate + '%');

    // Cập nhật thời gian làm việc
    $('#monthTime').text(data.month_time + ' giờ');

    // Cập nhật biểu đồ nếu có
    if (window.timeChart && data.months_data) {
        updateTimeChart(data.months_data);
    }
}

/**
 * Cập nhật danh sách dự án gần đây
 */
function updateProjects(projects) {
    const $projectsList = $('#projectsList');
    $projectsList.empty();

    if (!projects || projects.length === 0) {
        $projectsList.append('<div class="text-center py-4 text-muted">Không có dự án</div>');
        return;
    }

    projects.forEach(function(project) {
        // Xác định trạng thái dự án
        let statusClass = 'on-track';
        let statusText = 'Tiến độ tốt';

        if (project.status === 'warning') {
            statusClass = 'warning';
            statusText = 'Sắp đến hạn';
        } else if (project.status === 'overdue') {
            statusClass = 'overdue';
            statusText = 'Quá hạn';
        }

        // Tạo card dự án
        const projectCard = `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="project-card slide-in">
                    <div class="card-body">
                        <h5 class="project-title">
                            <a href="/projects/detail/${project.id}/">${project.name}</a>
                        </h5>
                        <span class="project-status ${statusClass}">${statusText}</span>
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: ${project.progress}%"
                                 aria-valuenow="${project.progress}" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                        <div class="project-meta">
                            <span>Tiến độ: ${project.progress}%</span>
                            <span>${project.days_left >= 0 ? 'Còn ' + project.days_left + ' ngày' : 'Quá hạn ' + Math.abs(project.days_left) + ' ngày'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        $projectsList.append(projectCard);
    });
}

/**
 * Cập nhật danh sách task sắp đến hạn
 */
function updateUpcomingTasks(tasks) {
    const $tasksList = $('#upcomingTasksList');
    $tasksList.empty();

    if (!tasks || tasks.length === 0) {
        $tasksList.append('<li class="list-group-item text-center text-muted">Không có task sắp đến hạn</li>');
        return;
    }

    tasks.forEach(function(task) {
        // Xác định trạng thái task
        let statusClass = '';

        if (task.status === 'To-do') {
            statusClass = 'bg-primary';
        } else if (task.status === 'In progress') {
            statusClass = 'bg-warning';
        } else if (task.status === 'Completed') {
            statusClass = 'bg-success';
        } else if (task.status === 'Late') {
            statusClass = 'bg-danger';
        }

        // Tạo item task
        const taskItem = `
            <li class="list-group-item fade-in">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="task-title">
                            <a href="/projects/tasks/${task.id}/">${task.title}</a>
                        </h6>
                        <div class="task-project">${task.project}</div>
                    </div>
                    <div class="text-end">
                        <span class="badge ${statusClass}">${task.status}</span>
                        <div class="task-deadline">${task.deadline}</div>
                    </div>
                </div>
            </li>
        `;

        $tasksList.append(taskItem);
    });
}

/**
 * Hiển thị hoặc ẩn loading
 */
function showLoading(show) {
    if (show) {
        $('#dashboardLoading').show();
        $('#dashboardContent').addClass('opacity-50');
    } else {
        $('#dashboardLoading').hide();
        $('#dashboardContent').removeClass('opacity-50');
    }
}

/**
 * Hiển thị thông báo lỗi
 */
function showErrorMessage(message) {
    const errorAlert = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    $('#dashboardAlerts').html(errorAlert);

    // Tự động ẩn sau 5 giây
    setTimeout(function() {
        $('#dashboardAlerts .alert').alert('close');
    }, 5000);
}
