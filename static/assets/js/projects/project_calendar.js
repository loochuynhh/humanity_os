/**
 * Project Calendar JavaScript
 * Quản lý lịch dự án, mốc thời gian, sự kiện và deadline
 */

$(document).ready(function() {
  // Khởi tạo lịch
  initCalendar();

  // Thiết lập bộ lọc dự án
  setupProjectFilters();

  // Thiết lập modals sự kiện
  setupEventModals();

  // Xử lý chuyển đổi chế độ xem (tháng/tuần)
  setupViewSwitcher();
});

/**
 * Khởi tạo lịch dự án
 */
function initCalendar() {
  // Sử dụng FullCalendar API
  var calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
    },
    locale: 'vi',
    buttonText: {
      today: 'Hôm nay',
      month: 'Tháng',
      week: 'Tuần',
      day: 'Ngày',
      list: 'Danh sách'
    },
    navLinks: true,
    editable: false,
    dayMaxEvents: true,
    events: function(info, successCallback, failureCallback) {
      loadEvents(info.start, info.end, successCallback, failureCallback);
    },
    eventClick: function(info) {
      showEventDetails(info.event);
    }
  });

  calendar.render();
  window.calendar = calendar;
}

/**
 * Tải dữ liệu sự kiện
 * @param {Date} start - Ngày bắt đầu
 * @param {Date} end - Ngày kết thúc
 * @param {Function} successCallback - Callback khi thành công
 * @param {Function} failureCallback - Callback khi thất bại
 */
function loadEvents(start, end, successCallback, failureCallback) {
  const projectId = $('#projectFilter').val();

  $.ajax({
    url: '/projects/project-calendar-events/',
    data: {
      start: start.toISOString(),
      end: end.toISOString(),
      project_id: projectId || ''
    },
    success: function(result) {
      successCallback(result);
    },
    error: function(error) {
      console.error('Lỗi khi tải sự kiện:', error);
      failureCallback([]);  // Gửi mảng rỗng để tránh lỗi
    }
  });
}

/**
 * Thiết lập bộ lọc dự án
 */
function setupProjectFilters() {
  // Sự kiện thay đổi dự án
  $('#projectFilter').on('change', function() {
    if (window.calendar) {
      window.calendar.refetchEvents();
    }
  });

  // Sự kiện thay đổi loại sự kiện
  $('.event-type-filter input[type="checkbox"]').on('change', function() {
    // Lấy danh sách các loại sự kiện đã chọn
    var selectedTypes = [];
    $('.event-type-filter input[type="checkbox"]:checked').each(function() {
      selectedTypes.push($(this).val());
    });

    // Lọc các sự kiện theo loại
    filterEventsByType(selectedTypes);
  });
}

/**
 * Lọc sự kiện theo loại
 * @param {Array} types - Mảng các loại sự kiện cần hiển thị
 */
function filterEventsByType(types) {
  if (types.length === 0) {
    // Nếu không có loại nào được chọn, hiển thị tất cả
    $('.calendar-event, .week-event').show();
    return;
  }

  // Ẩn tất cả sự kiện
  $('.calendar-event, .week-event').hide();

  // Hiển thị các sự kiện phù hợp
  types.forEach(function(type) {
    $('.calendar-event.' + type + ', .week-event.' + type).show();
  });
}

/**
 * Thiết lập chuyển đổi chế độ xem (tháng/tuần)
 */
function setupViewSwitcher() {
  // Sự kiện nút chế độ xem Tháng
  $('#monthViewBtn').on('click', function() {
    var currentDate = getCurrentViewDate();
    renderCalendarView(currentDate, 'month');
  });

  // Sự kiện nút chế độ xem Tuần
  $('#weekViewBtn').on('click', function() {
    var currentDate = getCurrentViewDate();
    renderCalendarView(currentDate, 'week');
  });
}

/**
 * Cập nhật trạng thái các nút chế độ xem
 * @param {string} view - Chế độ xem hiện tại
 */
function updateViewButtons(view) {
  $('.calendar-view-selector .btn').removeClass('active');

  if (view === 'month') {
    $('#monthViewBtn').addClass('active');
  } else if (view === 'week') {
    $('#weekViewBtn').addClass('active');
  }
}

/**
 * Lấy ngày đang xem hiện tại
 * @returns {Date} Ngày đang xem
 */
function getCurrentViewDate() {
  var titleText = $('.calendar-title').text();
  var monthNames = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];

  var parts = titleText.split(' ');
  var month = monthNames.indexOf(parts[0] + ' ' + parts[1]);
  var year = parseInt(parts[2]);

  return new Date(year, month, 1);
}

/**
 * Thiết lập modals sự kiện
 */
function setupEventModals() {
  // Đảm bảo các modal được khởi tạo
  var eventModal = new bootstrap.Modal(document.getElementById('eventModal'), {
    keyboard: true
  });

  var dayEventsModal = new bootstrap.Modal(document.getElementById('dayEventsModal'), {
    keyboard: true
  });
}

/**
 * Hiển thị chi tiết sự kiện
 * @param {Object} event - Sự kiện cần hiển thị chi tiết
 */
function showEventDetails(event) {
  // Cập nhật thông tin sự kiện vào modal
  $('#eventTitle').text(event.title);
  $('#eventStart').text(formatDate(event.start));
  $('#eventEnd').text(event.end ? formatDate(event.end) : formatDate(event.start));
  $('#eventProject').text(event.extendedProps.project || 'Không có');
  $('#eventDescription').text(event.extendedProps.description || 'Không có mô tả');

  // Kiểm tra có phải task không
  if (event.extendedProps.type === 'task') {
    $('#taskDetails').removeClass('d-none');
    $('#eventStatus').text(event.extendedProps.status || 'Không có');
    $('#eventStatus').attr('class', getStatusClass(event.extendedProps.status));
    $('#eventAssignees').text(event.extendedProps.assignees || 'Không có');

    // Hiển thị nút xem chi tiết nếu có link
    if (event.url) {
      $('#eventLink').attr('href', event.url).removeClass('d-none');
    } else {
      $('#eventLink').addClass('d-none');
    }
  } else {
    $('#taskDetails').addClass('d-none');
    $('#eventLink').addClass('d-none');
  }

  // Hiển thị modal bằng Bootstrap 5 API
  var modal = document.getElementById('eventModal');
  if (modal) {
    var bsModal = new bootstrap.Modal(modal);
    bsModal.show();
  }
}

/**
 * Định dạng ngày tháng
 * @param {Date} date - Ngày cần định dạng
 * @returns {string} Chuỗi ngày đã định dạng
 */
function formatDate(date) {
  if (!date) return '';
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return date.toLocaleDateString('vi-VN', options);
}

/**
 * Lấy class tương ứng với trạng thái
 * @param {string} status - Trạng thái task
 * @returns {string} Class CSS tương ứng
 */
function getStatusClass(status) {
  if (!status) return '';
  
  status = status.toLowerCase();
  if (status.includes('completed') || status.includes('hoàn thành'))
    return 'badge bg-success';
  else if (status.includes('progress') || status.includes('đang'))
    return 'badge bg-warning';
  else if (status.includes('late') || status.includes('trễ'))
    return 'badge bg-danger';
  else if (status.includes('todo') || status.includes('chưa'))
    return 'badge bg-secondary';
  else
    return 'badge bg-primary';
}

/**
 * Hiển thị tất cả sự kiện trong một ngày
 * @param {string} date - Ngày cần hiển thị sự kiện (YYYY-MM-DD)
 */
function showDayEvents(date) {
  $.ajax({
    url: '/projects/day-events/',
    method: 'GET',
    data: { date: date },
    dataType: 'json',
    success: function(response) {
      // Cập nhật nội dung modal
      var modal = $('#dayEventsModal');
      var eventsList = modal.find('.day-events-list');

      // Định dạng lại ngày
      var formattedDate = formatDate(date);
      modal.find('.modal-title').text('Sự kiện ngày ' + formattedDate);

      // Xóa danh sách cũ
      eventsList.empty();

      // Thêm các sự kiện vào danh sách
      if (response.events && response.events.length > 0) {
        response.events.forEach(function(event) {
          var eventHtml = `
            <div class="day-event-item ${event.type}">
              <div class="event-time">${event.start_time || ''} ${event.end_time ? '- ' + event.end_time : ''}</div>
              <div class="event-title">${event.title}</div>
              <div class="event-project">${event.project_name}</div>
              <button class="btn btn-sm btn-outline-primary view-details" data-event-id="${event.id}">
                Xem chi tiết
              </button>
            </div>
          `;

          eventsList.append(eventHtml);
        });

        // Thêm sự kiện click cho các nút xem chi tiết
        eventsList.find('.view-details').on('click', function() {
          var eventId = $(this).data('event-id');

          // Đóng modal hiện tại
          var dayEventsModal = bootstrap.Modal.getInstance(document.getElementById('dayEventsModal'));
          dayEventsModal.hide();

          // Hiển thị chi tiết sự kiện
          setTimeout(function() {
            showEventDetails(eventId);
          }, 500);
        });
      } else {
        eventsList.append('<p>Không có sự kiện nào trong ngày này</p>');
      }

      // Hiển thị modal
      var dayEventsModal = new bootstrap.Modal(document.getElementById('dayEventsModal'));
      dayEventsModal.show();
    },
    error: function(xhr, status, error) {
      console.error('Lỗi khi tải sự kiện trong ngày:', error);
      showErrorNotification('Không thể tải sự kiện trong ngày. Vui lòng thử lại sau.');
    }
  });
}

/**
 * Hiển thị thông báo lỗi
 * @param {string} message - Nội dung thông báo
 */
function showErrorNotification(message) {
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
