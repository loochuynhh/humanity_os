/**
 * Humanity OS - Project Task Board (Kanban) JavaScript
 * Quản lý chức năng drag & drop và tương tác trên bảng Kanban
 */

$(document).ready(function() {
    // Khởi tạo Sortable.js cho các cột Kanban
    initKanbanBoard();

    // Lấy dữ liệu Kanban từ API
    loadKanbanData();

    // Xử lý sự kiện chọn dự án
    $('#projectFilter').change(function() {
        const projectId = $(this).val();
        loadKanbanData(projectId);
    });

    // Xử lý mở modal chi tiết task
    $(document).on('click', '.kanban-card', function(e) {
        if ($(e.target).hasClass('task-action') || $(e.target).parents('.task-action').length) {
            return; // Không mở modal nếu đang click vào các nút hành động
        }
        const taskId = $(this).data('id');
        showTaskModal(taskId);
    });

    // Xử lý nút refresh
    $('#refreshKanban').click(function() {
        const projectId = $('#projectFilter').val();
        loadKanbanData(projectId);
    });
});

/**
 * Khởi tạo Sortable.js cho các cột Kanban
 */
function initKanbanBoard() {
    // Tạo Sortable cho từng cột
    const columns = document.querySelectorAll('.kanban-column');
    columns.forEach(column => {
        new Sortable(column, {
            group: 'tasks',
            animation: 150,
            ghostClass: 'kanban-card-ghost',
            chosenClass: 'kanban-card-chosen',
            dragClass: 'kanban-card-drag',
            onEnd: function(evt) {
                const taskId = evt.item.getAttribute('data-id');
                const newStatus = evt.to.getAttribute('data-status');
                updateTaskStatus(taskId, newStatus);
            }
        });
    });
}

/**
 * Tải dữ liệu Kanban từ API
 */
function loadKanbanData(projectId = '') {
    // Hiển thị loading
    showLoading(true);

    // URL API
    let url = '/projects/api/project-tasks/';
    if (projectId) {
        url += projectId + '/';
    }

    // Gọi API
    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            // Cập nhật từng cột
            updateKanbanColumn('todo', response.todo);
            updateKanbanColumn('in_progress', response.in_progress);
            updateKanbanColumn('completed', response.completed);
            updateKanbanColumn('late', response.late);

            // Cập nhật số lượng task
            updateTaskCounts(response);

            // Ẩn loading
            showLoading(false);
        },
        error: function(xhr, status, error) {
            console.error('Error loading Kanban data:', error);
            showLoading(false);
            showErrorMessage('Không thể tải dữ liệu bảng Kanban. Vui lòng thử lại sau.');
        }
    });
}

/**
 * Cập nhật số lượng task của mỗi cột
 */
function updateTaskCounts(data) {
    $('#todoCount').text(data.todo.length);
    $('#inProgressCount').text(data.in_progress.length);
    $('#completedCount').text(data.completed.length);
    $('#lateCount').text(data.late.length);
    $('#totalCount').text(data.todo.length + data.in_progress.length + data.completed.length + data.late.length);
}

/**
 * Cập nhật nội dung của một cột Kanban
 */
function updateKanbanColumn(columnId, tasks) {
    const $column = $(`#${columnId}Column`);
    $column.empty();

    if (tasks.length === 0) {
        $column.append(`
            <div class="kanban-empty text-center py-3">
                <p class="text-muted mb-0"><i class="bi bi-inbox"></i> Không có task</p>
            </div>
        `);
        return;
    }

    tasks.forEach(task => {
        const assignees = task.assignees.map(user => {
            return `<div class="kanban-avatar" data-bs-toggle="tooltip" title="${user.name}">
                <img src="${user.avatar}" alt="${user.name}" class="rounded-circle">
            </div>`;
        }).join('');

        // Trạng thái dựa trên deadline
        let deadlineClass = '';
        let deadlineIcon = '';

        if (task.is_overdue) {
            deadlineClass = 'text-danger';
            deadlineIcon = '<i class="bi bi-exclamation-circle-fill"></i> ';
        } else if (task.days_until_deadline <= 2) {
            deadlineClass = 'text-warning';
            deadlineIcon = '<i class="bi bi-clock-fill"></i> ';
        }

        // Tạo card
        const cardHtml = `
            <div class="kanban-card" data-id="${task.id}">
                <div class="kanban-card-header">
                    <span class="kanban-project-badge">${task.project_name}</span>
                    <span class="kanban-difficulty ${task.difficulty.toLowerCase()}">${task.difficulty}</span>
                </div>
                <h6 class="kanban-card-title">${task.title}</h6>
                <p class="kanban-card-description">${task.description.length > 80 ? task.description.substring(0, 77) + '...' : task.description}</p>
                <div class="kanban-card-footer">
                    <div class="kanban-deadline ${deadlineClass}">
                        ${deadlineIcon}${task.deadline}
                    </div>
                    <div class="kanban-assignees">
                        ${assignees}
                    </div>
                </div>
                <div class="kanban-card-actions">
                    <button class="btn btn-sm btn-icon task-action" onclick="showTaskModal(${task.id})" data-bs-toggle="tooltip" title="Xem chi tiết">
                        <i class="bi bi-eye"></i>
                    </button>
                </div>
            </div>
        `;

        $column.append(cardHtml);
    });

    // Khởi tạo lại tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
}

/**
 * Cập nhật trạng thái của task
 */
function updateTaskStatus(taskId, newStatus) {
    // Mapping các trạng thái
    const statusMapping = {
        'todo': 'To-do',
        'in_progress': 'In progress',
        'completed': 'Completed',
        'late': 'Late'
    };

    // Hiển thị loading
    showLoading(true);

    // Gọi API cập nhật
    $.ajax({
        url: '/projects/api/update-task-status/',
        method: 'POST',
        data: {
            task_id: taskId,
            status: statusMapping[newStatus],
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            showLoading(false);
            if (response.success) {
                showSuccessMessage(`Đã cập nhật trạng thái task sang: ${statusMapping[newStatus]}`);

                // Nếu cần làm mới dữ liệu
                const projectId = $('#projectFilter').val();
                loadKanbanData(projectId);
            } else {
                showErrorMessage(response.error || 'Cập nhật trạng thái thất bại');

                // Làm mới dữ liệu để reset vị trí card
                loadKanbanData(projectId);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error updating task status:', error);
            showLoading(false);
            showErrorMessage('Không thể cập nhật trạng thái task. Vui lòng thử lại.');

            // Làm mới dữ liệu để reset vị trí card
            const projectId = $('#projectFilter').val();
            loadKanbanData(projectId);
        }
    });
}

/**
 * Hiển thị modal chi tiết task
 */
function showTaskModal(taskId) {
    // Mở modal
    $('#taskDetailModal').modal('show');

    // Hiển thị loading trong modal
    $('#taskModalContent').html(`
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
            </div>
            <p class="mt-2">Đang tải thông tin task...</p>
        </div>
    `);

    // Gọi API lấy chi tiết task
    $.ajax({
        url: `/projects/tasks/${taskId}/`,
        method: 'GET',
        success: function(response) {
            $('#taskModalContent').html(response);

            // Khởi tạo các sự kiện trong modal
            initTaskModalEvents();
        },
        error: function(xhr, status, error) {
            console.error('Error loading task details:', error);
            $('#taskModalContent').html(`
                <div class="text-center py-5 text-danger">
                    <i class="bi bi-exclamation-triangle-fill fa-3x mb-3"></i>
                    <p>Không thể tải thông tin task. Vui lòng thử lại sau.</p>
                    <button type="button" class="btn btn-primary mt-3" data-bs-dismiss="modal">Đóng</button>
                </div>
            `);
        }
    });
}

/**
 * Khởi tạo các sự kiện trong modal chi tiết task
 */
function initTaskModalEvents() {
    // Các sự kiện JS cho modal task detail
    // ...
}

/**
 * Hiển thị hoặc ẩn loading
 */
function showLoading(show) {
    if (show) {
        $('#kanbanLoading').show();
        $('#kanbanContent').addClass('opacity-50');
    } else {
        $('#kanbanLoading').hide();
        $('#kanbanContent').removeClass('opacity-50');
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

    $('#kanbanAlerts').html(errorAlert);

    // Tự động ẩn sau 5 giây
    setTimeout(function() {
        $('#kanbanAlerts .alert').alert('close');
    }, 5000);
}

/**
 * Hiển thị thông báo thành công
 */
function showSuccessMessage(message) {
    const successAlert = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <i class="bi bi-check-circle-fill me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    $('#kanbanAlerts').html(successAlert);

    // Tự động ẩn sau 3 giây
    setTimeout(function() {
        $('#kanbanAlerts .alert').alert('close');
    }, 3000);
}
