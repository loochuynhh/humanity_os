/**
 * Project Calendar JavaScript
 * Humanity OS
 */
document.addEventListener('DOMContentLoaded', function() {
  // Khởi tạo biến
  let calendar;
  let currentView = 'dayGridMonth'; // Mặc định xem theo tháng
  let selectedProjectId = '';
  
  // Các phần tử DOM
  const calendarEl = document.getElementById('calendar');
  const projectFilter = document.getElementById('projectFilter');
  const viewMonthBtn = document.getElementById('viewMonth');
  const viewWeekBtn = document.getElementById('viewWeek');
  const viewListBtn = document.getElementById('viewList');
  const calendarTitle = document.getElementById('calendarTitle');
  
  // Khởi tạo FullCalendar
  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: currentView,
    headerToolbar: {
      left: 'prev,next today',
      center: '',
      right: ''
    },
    locale: 'vi',
    firstDay: 1, // Thứ 2 là ngày đầu tuần
    height: 'auto',
    allDaySlot: false,
    slotMinTime: '00:00:00',
    slotMaxTime: '24:00:00',    
    slotDuration: '00:30:00',
    dayMaxEvents: 3, // Số sự kiện tối đa hiển thị trước khi hiện "+ more"
    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    },
    views: {
      dayGridMonth: {
        dayMaxEventRows: 3
      },
      timeGridWeek: {
        dayHeaderFormat: { weekday: 'short', day: 'numeric', month: 'numeric' },
        slotEventOverlap: false // Không cho phép sự kiện chồng lên nhau
      },
      listWeek: {
        listDayFormat: { weekday: 'long', day: 'numeric', month: 'long' },
        listDaySideFormat: false
      }
    },
    nowIndicator: true,
    eventDisplay: 'block',
    events: function(info, successCallback, failureCallback) {
      // Lấy sự kiện từ API
      const params = new URLSearchParams({
        start: info.startStr,
        end: info.endStr
      });
      
      if (selectedProjectId) {
        params.append('project_id', selectedProjectId);
      }
      
      fetch(`${calendarEventsUrl}?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
          // Sử dụng cùng một màu cho tất cả các sự kiện
          const events = data.events.map(event => {
            return {
              ...event,
              backgroundColor: 'rgba(13, 110, 253, 0.2)',
              borderColor: '#0d6efd',
              textColor: '#0d6efd'
            };
          });
          
          successCallback(events);
          updateCalendarTitle();
        })
        .catch(error => {
          console.error('Error fetching calendar events:', error);
          failureCallback(error);
        });
    },
    eventClick: function(info) {
      handleEventClick(info.event);
    },
    moreLinkClick: function(info) {
      showDayEntriesModal(info.date, info.allSegs.map(seg => seg.event));
      return false; // Ngăn không cho FullCalendar xử lý mặc định
    },
    datesSet: function() {
      updateCalendarTitle();
    }
  });
  
  // Render lịch
  calendar.render();
  
  // Cập nhật tiêu đề lịch
  function updateCalendarTitle() {
    const dateTitle = calendar.view.title;
    calendarTitle.textContent = dateTitle;
  }
  
  // Hàm xóa popover nếu nó xuất hiện
  function removePopover() {
    const popovers = document.querySelectorAll('.fc-popover, .fc-more-popover, div[class*="fc-popover"]');
    if (popovers.length > 0) {
      popovers.forEach(popover => {
        popover.remove();
      });
    }
  }
  
  // Theo dõi và xóa popover
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.addedNodes.length) {
        for (let i = 0; i < mutation.addedNodes.length; i++) {
          const node = mutation.addedNodes[i];
          if (node.classList && 
              (node.classList.contains('fc-popover') || 
               node.classList.contains('fc-more-popover') || 
               (node.className && node.className.includes('fc-popover')))) {
            node.remove();
          }
        }
      }
    });
  });
  
  // Bắt đầu theo dõi DOM
  observer.observe(document.body, { 
    childList: true,
    subtree: true
  });
  
  // Thêm sự kiện click cho nút "more" để đảm bảo popover không xuất hiện
  document.addEventListener('click', function(e) {
    if (e.target && e.target.classList && 
        (e.target.classList.contains('fc-daygrid-more-link') || 
         e.target.closest('.fc-daygrid-more-link'))) {
      setTimeout(removePopover, 0);
    }
  }, true);
  
  // Xóa popover nếu nó đã tồn tại
  removePopover();
  
  // Xử lý khi click vào sự kiện
  function handleEventClick(event) {
    const extendedProps = event.extendedProps;
    
    if (extendedProps.type === 'time_entry') {
      // Hiển thị modal chi tiết time entry
      const modal = document.getElementById('timeEntryDetailModal');
      const modalInstance = new bootstrap.Modal(modal);
      
      // Cập nhật nội dung modal
      modal.querySelector('.time-entry-task-title').textContent = extendedProps.task_title;
      modal.querySelector('.time-entry-project').textContent = extendedProps.project;
      modal.querySelector('.time-entry-user').textContent = extendedProps.user;
      modal.querySelector('.time-entry-start-time').textContent = extendedProps.start_time_formatted;
      modal.querySelector('.time-entry-end-time').textContent = extendedProps.end_time_formatted || 'Đang thực hiện';
      modal.querySelector('.time-entry-duration').textContent = `${extendedProps.duration.toFixed(2)} giờ`;
      modal.querySelector('.time-entry-role').textContent = extendedProps.role || 'Không xác định';
      
      // Cập nhật link xem task
      const viewTaskBtn = modal.querySelector('.view-task-btn');
      viewTaskBtn.href = `/projects/task/${extendedProps.task_id}/`;
      
      // Hiển thị modal
      modalInstance.show();
    }
  }
  
  // Hiển thị modal danh sách time entries trong ngày
  function showDayEntriesModal(date, events) {
    const modal = document.getElementById('dayEntriesModal');
    const modalInstance = new bootstrap.Modal(modal);
    const entriesList = modal.querySelector('.day-entries-list');
    const dateDisplay = modal.querySelector('.day-entries-date');
    
    // Định dạng ngày
    const formattedDate = new Date(date).toLocaleDateString('vi-VN', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
    
    dateDisplay.textContent = formattedDate;
    
    // Xóa danh sách cũ
    entriesList.innerHTML = '';
    
    // Sắp xếp sự kiện theo thời gian bắt đầu
    events.sort((a, b) => new Date(a.start) - new Date(b.start));
    
    // Tạo danh sách mới
    if (events.length === 0) {
      entriesList.innerHTML = `
        <div class="list-group-item text-center py-4">
          <i class="bi bi-calendar-x text-muted mb-2" style="font-size: 2rem;"></i>
          <p class="mb-0 text-muted">Không có time entry nào trong ngày này</p>
        </div>
      `;
    } else {
      events.forEach(event => {
        const props = event.extendedProps;
        const startTime = props.start_time_formatted;
        const endTime = props.end_time_formatted || 'Đang thực hiện';
        const duration = props.duration.toFixed(2);
        
        const entryItem = document.createElement('a');
        entryItem.href = '#';
        entryItem.className = 'list-group-item list-group-item-action';
        entryItem.innerHTML = `
          <div class="d-flex w-100 justify-content-between align-items-center">
            <h6 class="mb-1">${props.task_title}</h6>
            <span class="badge bg-primary">${props.project}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <small class="text-muted">${props.user}</small>
              <small class="text-muted ms-2">${startTime} - ${endTime}</small>
            </div>
            <span class="badge bg-light text-dark">${duration} giờ</span>
          </div>
        `;
        
        // Xử lý sự kiện click
        entryItem.addEventListener('click', function(e) {
          e.preventDefault();
          modalInstance.hide();
          
          // Hiển thị modal chi tiết
          setTimeout(() => {
            handleEventClick(event);
          }, 500);
        });
        
        entriesList.appendChild(entryItem);
      });
    }
    
    // Hiển thị modal
    modalInstance.show();
  }
  
  // Xử lý chuyển đổi chế độ xem
  viewMonthBtn.addEventListener('click', function() {
    setActiveView('dayGridMonth', this);
  });
  
  viewWeekBtn.addEventListener('click', function() {
    setActiveView('timeGridWeek', this);
  });
  
  viewListBtn.addEventListener('click', function() {
    setActiveView('listWeek', this);
  });
  
  function setActiveView(view, button) {
    // Cập nhật chế độ xem hiện tại
    currentView = view;
    calendar.changeView(view);
    
    // Cập nhật trạng thái nút
    viewMonthBtn.classList.remove('active');
    viewWeekBtn.classList.remove('active');
    viewListBtn.classList.remove('active');
    button.classList.add('active');
    
    // Cập nhật tiêu đề
    updateCalendarTitle();
  }
  
  // Xử lý lọc theo dự án
  projectFilter.addEventListener('change', function() {
    selectedProjectId = this.value;
    calendar.refetchEvents();
  });
  
  // Cập nhật kích thước lịch khi thay đổi kích thước cửa sổ
  window.addEventListener('resize', function() {
    calendar.updateSize();
  });
  
  // Khởi tạo tooltips cho các nút
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}); 