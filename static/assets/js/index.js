/**
 * Initialize Task Chart (Doughnut)
 * Expects data: [To_do, In_progress, Completed]
 */
function initTaskChart(data) {
  const taskCtx = document.getElementById("taskChart").getContext("2d");
  const chartData = Array.isArray(data) && data.length >= 3 ? data.slice(0, 3) : [0, 0, 0];
  new Chart(taskCtx, {
      type: "doughnut",
      data: {
          labels: ["To-do", "Đang làm", "Hoàn thành"],
          datasets: [{
              data: chartData,
              backgroundColor: ["#0d6efd", "#ffc107", "#198754"],
              borderWidth: 1
          }]
      },
      options: {
          plugins: {
              legend: { position: "bottom" },
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          const label = context.label || '';
                          const value = context.raw || 0;
                          const total = context.dataset.data.reduce((a, b) => a + b, 0);
                          const percentage = total ? Math.round((value / total) * 100) : 0;
                          return `${label}: ${value} (${percentage}%)`;
                      }
                  }
              }
          },
          cutout: '65%'
      }
  });
}

/**
* Initialize Time Chart (Line)
* Expects data: [hours for Mon, Tue, Wed, Thu, Fri, Sat, Sun]
*/
function initTimeChart(data) {
  const timeCtx = document.getElementById("timeChart").getContext("2d");
  const chartData = Array.isArray(data) && data.length === 7 ? data : [0, 0, 0, 0, 0, 0, 0];
  new Chart(timeCtx, {
      type: "line",
      data: {
          labels: ["T2", "T3", "T4", "T5", "T6", "T7", "CN"],
          datasets: [{
              label: "Giờ làm",
              data: chartData,
              borderColor: "#0d6efd",
              backgroundColor: "rgba(13, 110, 253, 0.1)",
              fill: true,
              tension: 0.3,
              borderWidth: 2,
              pointBackgroundColor: "#0d6efd",
              pointRadius: 4
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true,
                  ticks: {
                      callback: function(value) {
                          return value + 'h';
                      }
                  }
              }
          },
          plugins: {
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          return context.parsed.y.toFixed(1) + ' giờ';
                      }
                  }
              }
          }
      }
  });
}

/**
* Initialize Project Time Allocation Chart (Pie)
* Expects data: { labels: [project_name, ...], data: [hours, ...] }
*/
function initProjectTimeChart(data) {
  const projectTimeCtx = document.getElementById("projectTimeChart").getContext("2d");
  const chartData = data && data.labels && data.data ? {
      labels: data.labels.length ? data.labels : ['Không có dự án'],
      data: data.data.length ? data.data : [1]
  } : {
      labels: ['Không có dự án'],
      data: [1]
  };
  new Chart(projectTimeCtx, {
      type: "pie",
      data: {
          labels: chartData.labels,
          datasets: [{
              data: chartData.data,
              backgroundColor: ["#0d6efd", "#ffc107", "#198754", "#dc3545", "#6f42c1"],
              borderWidth: 1
          }]
      },
      options: {
          plugins: {
              legend: { position: "bottom" },
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          const label = context.label || '';
                          const value = context.raw || 0;
                          const total = context.dataset.data.reduce((a, b) => a + b, 0);
                          const valueRounded = Number(value).toFixed(2);
                          const percentage = total ? ((value / total) * 100).toFixed(2) : "0.00";
                          return `${label}: ${valueRounded}h (${percentage}%)`;
                      }
                  }
              }
          }
      }
  });
}

/**
* Show error message in modal
*/
function showError(errorDivId, message) {
  const errorDiv = document.getElementById(errorDivId);
  if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.classList.remove('d-none');
      setTimeout(() => errorDiv.classList.add('d-none'), 5000);
  }
}

/**
* Setup webcam for check-in/check-out
*/
function setupWebcam(modalId, videoId, canvasId, snapButtonId, imageDataId, previewId, submitButtonId, loadingId) {
  const modal = document.getElementById(modalId);
  const video = document.getElementById(videoId);
  const canvas = document.getElementById(canvasId);
  const snapButton = document.getElementById(snapButtonId);
  const imageDataInput = document.getElementById(imageDataId);
  const previewImg = document.getElementById(previewId);
  const submitButton = document.getElementById(submitButtonId);
  const loading = document.getElementById(loadingId);
  let stream = null;
  let hasImage = false;

  if (!modal || !video || !canvas || !snapButton || !imageDataInput || !previewImg || !submitButton || !loading) {
      console.error('Thiếu phần tử trong setupWebcam');
      return;
  }

  modal.addEventListener('shown.bs.modal', () => {
      loading.style.display = 'block';
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(s => {
              stream = s;
              video.srcObject = stream;
              loading.style.display = 'none';
          })
          .catch(err => {
              loading.style.display = 'none';
              console.error('Lỗi webcam:', err);
          });
  });

  modal.addEventListener('hidden.bs.modal', () => {
      if (stream) {
          stream.getTracks().forEach(track => track.stop());
      }
      // Reset trạng thái
      video.style.display = 'block';
      previewImg.classList.add('d-none');
      imageDataInput.value = '';
      hasImage = false;
      snapButton.textContent = 'Chụp ảnh';
  });

  snapButton.addEventListener('click', () => {
      if (!hasImage) {
          // Chụp ảnh
          if (!video.srcObject) {
              console.error('Video stream không khả dụng');
              return;
          }

          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7);
          imageDataInput.value = compressedDataUrl;
          previewImg.src = compressedDataUrl;
          previewImg.classList.remove('d-none');
          video.style.display = 'none';

          hasImage = true;
          snapButton.textContent = 'Chụp lại';
      } else {
          // Chụp lại
          video.style.display = 'block';
          previewImg.classList.add('d-none');
          imageDataInput.value = '';
          hasImage = false;
          snapButton.textContent = 'Chụp ảnh';
      }

      // Kiểm tra để kích hoạt nút submit
      const locationInput = document.getElementById(modalId === 'checkInModal' ? 'checkin_location' : 'checkout_location');
      const submitButton = document.getElementById(modalId === 'checkInModal' ? 'checkin_submit' : 'checkout_submit');
      if (submitButton) {
          submitButton.disabled = !imageDataInput.value || !locationInput?.value;
      }
  });
}

/**
* Setup geolocation for check-in/check-out
*/
function setupGeolocation(modalId, inputId, loadingId) {
  const modal = document.getElementById(modalId);
  const input = document.getElementById(inputId);
  const loading = document.getElementById(loadingId);
  const submitButtonId = modalId === 'checkInModal' ? 'checkin_submit' : 'checkout_submit';
  const submitButton = document.getElementById(submitButtonId);

  if (!modal || !input || !loading || !submitButton) {
      console.error('Thiếu phần tử trong setupGeolocation:', { modalId, inputId, loadingId, submitButtonId });
      showError(modalId + '_error', 'Lỗi lấy vị trí. Vui lòng thử lại.');
      return;
  }

  modal.addEventListener('shown.bs.modal', () => {
      if (navigator.geolocation) {
          loading.classList.remove('d-none');
          navigator.geolocation.getCurrentPosition(
              position => {
                  const lat = position.coords.latitude;
                  const lon = position.coords.longitude;
                  input.value = `${lat},${lon}`;
                  loading.classList.add('d-none');
                  const imageDataInput = document.getElementById(modalId === 'checkInModal' ? 'checkin_image_data' : 'checkout_image_data');
                  submitButton.disabled = !input.value || !imageDataInput?.value;
              },
              error => {
                  loading.classList.add('d-none');
                  showError(modalId + '_error', 'Không thể lấy vị trí: ' + error.message);
              }
          );
      } else {
          showError(modalId + '_error', 'Trình duyệt không hỗ trợ lấy vị trí.');
      }
  });
}

/**
* Initialize all charts and features
*/
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded - initializing scripts');

  function initChart(elementId, initFunction, expectedType) {
      const element = document.getElementById(elementId);
      if (!element) {
          console.warn(`Không tìm thấy phần tử ${elementId}`);
          return;
      }

      let chartData;
      if (elementId === 'projectTimeChart') {
          chartData = window.djangoChartData ? window.djangoChartData[elementId] : null;
      } else {
          chartData = element.dataset.chartData;
      }

      console.log(`${elementId} data:`, chartData);

      if (!chartData || (typeof chartData === 'string' && (chartData.trim() === '' || chartData === '{' || chartData === '{}'))) {
          console.warn(`Dữ liệu không hợp lệ hoặc rỗng cho ${elementId}`);
          initFunction(expectedType === 'array' ? [] : { labels: ['Không có dữ liệu'], data: [1] });
          return;
      }

      try {
          let parsedData;
          if (elementId === 'projectTimeChart') {
              parsedData = chartData;
          } else {
              parsedData = JSON.parse(chartData);
          }

          if (expectedType === 'object') {
              if (!parsedData || !parsedData.labels || !parsedData.data || !Array.isArray(parsedData.labels) || !Array.isArray(parsedData.data)) {
                  console.warn(`Dữ liệu object không đúng định dạng cho ${elementId}:`, parsedData);
                  initFunction({ labels: ['Không có dữ liệu'], data: [1] });
                  return;
              }
          }
          initFunction(parsedData);
      } catch (e) {
          console.error(`Lỗi parse dữ liệu cho ${elementId}:`, e.message, chartData);
          initFunction(expectedType === 'array' ? [] : { labels: ['Không có dữ liệu'], data: [1] });
      }
  }

  initChart('taskChart', initTaskChart, 'array');
  initChart('timeChart', initTimeChart, 'array');
  initChart('projectTimeChart', initProjectTimeChart, 'object');

  // Initialize webcam and geolocation
  console.log('Setting up webcam and geolocation');
  if (document.getElementById('checkInModal')) {
      setupWebcam(
          'checkInModal',
          'checkin_video',
          'checkin_canvas',
          'checkin_snap',
          'checkin_image_data',
          'checkin_preview',
          'checkin_submit',
          'checkin_loading'
      );
      setupGeolocation('checkInModal', 'checkin_location', 'checkin_location_loading');
  }

  if (document.getElementById('checkOutModal')) {
      setupWebcam(
          'checkOutModal',
          'checkout_video',
          'checkout_canvas',
          'checkout_snap',
          'checkout_image_data',
          'checkout_preview',
          'checkout_submit',
          'checkout_loading'
      );
      setupGeolocation('checkOutModal', 'checkout_location', 'checkout_location_loading');
  }

  // Xử lý nút check-in
  console.log('Setting up check-in button handler');
  const checkInBtn = document.getElementById('checkin_submit');

  if (checkInBtn) {
      console.log('Found check-in button:', checkInBtn);
      checkInBtn.addEventListener('click', handleCheckInClick);
  } else {
      console.warn('Check-in button not found!');
  }

  // Xử lý nút check-out
  console.log('Setting up check-out button handler');
  const checkOutBtn = document.getElementById('checkout_submit');

  if (checkOutBtn) {
      console.log('Found check-out button:', checkOutBtn);
      checkOutBtn.addEventListener('click', handleCheckOutClick);
  } else {
      console.warn('Check-out button not found!');
  }

  // Thêm event listener để đảm bảo các modal được khởi tạo đúng cách
  const checkInModal = document.getElementById('checkInModal');
  if (checkInModal) {
      checkInModal.addEventListener('shown.bs.modal', function() {
          console.log('Check-in modal shown');
      });
  }

  const checkOutModal = document.getElementById('checkOutModal');
  if (checkOutModal) {
      checkOutModal.addEventListener('shown.bs.modal', function() {
          console.log('Check-out modal shown');
      });
  }
});

/**
* Cập nhật thông tin thời gian làm việc mà không cần tải lại trang
*/
function updateWorkTimeDisplay() {
  // Gửi AJAX request để lấy thời gian làm việc hiện tại
  fetch('/api/current-work-time/', {
      method: 'GET',
      credentials: 'same-origin',
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Cập nhật thời gian hiển thị trên trang chủ
          const todayTimeDisplay = document.getElementById('today-time-display');
          if (todayTimeDisplay) {
              todayTimeDisplay.textContent = data.today_time;
          }

          // Cập nhật thông tin khác nếu cần
          const timeCard = document.querySelector('.card-body p.text-muted:first-of-type');
          if (timeCard) {
              timeCard.innerHTML = 'Hôm nay: <span class="fw-bold">' + data.today_time + '</span>';
          }
      }
  })
  .catch(error => {
      console.error('Error fetching work time:', error);
  });
}

/**
* Xử lý sau khi check-in/check-out thành công
*/
function handleSuccessfulAttendance(type) {
  // Cập nhật UI mà không cần reload
  updateWorkTimeDisplay();

  // Cập nhật nút check-in/check-out theo trạng thái mới nếu cần
  const checkInBtn = document.querySelector('button[data-bs-target="#checkInModal"]');
  const checkOutBtn = document.querySelector('button[data-bs-target="#checkOutModal"]');

  if (type === 'checkin') {
      // Đã check-in, disable nút check-in và enable nút check-out
      if (checkInBtn) checkInBtn.classList.add('disabled');
      if (checkOutBtn) checkOutBtn.classList.remove('disabled');
  } else if (type === 'checkout') {
      // Đã check-out, disable cả hai nút
      if (checkInBtn) checkInBtn.classList.add('disabled');
      if (checkOutBtn) checkOutBtn.classList.add('disabled');
  }
}

/**
 * Xử lý sự kiện click nút check-in
 */
function handleCheckInClick() {
  console.log('handleCheckInClick called');

  const checkInForm = document.getElementById('checkInForm');
  const submitBtn = document.getElementById('checkin_submit');
  const errorDiv = document.getElementById('checkin_error');

  if (!checkInForm || !submitBtn) {
    console.error('Check-in form or submit button not found');
    return;
  }

  // Kiểm tra nếu nút đang bị disable để tránh click liên tục
  if (submitBtn.disabled) {
    console.log('Submit button is disabled, ignoring click');
    return;
  }

  // Lấy dữ liệu form
  const formData = new FormData(checkInForm);

  // Kiểm tra dữ liệu
  const imageData = formData.get('checkin_image');
  const location = formData.get('checkin_location');

  console.log('Check-in data:', {
    'Has image': !!imageData,
    'Has location': !!location,
    'Image data length': imageData ? imageData.length : 0,
    'Location value': location || 'empty'
  });

  if (!imageData || !location) {
    errorDiv.textContent = 'Vui lòng chụp ảnh và cho phép truy cập vị trí';
    errorDiv.classList.remove('d-none');
    return;
  }

  // Disable nút ngay lập tức để ngăn click liên tục
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Đang xử lý...';
  errorDiv.classList.add('d-none');

  // Gửi request
  const url = checkInForm.getAttribute('action');
  console.log('Sending check-in request to:', url);

  // Thêm CSRF token vào FormData
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  formData.append('csrfmiddlewaretoken', csrfToken);

  fetch(url, {
    method: 'POST',
    body: formData,
    credentials: 'same-origin',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken // Đảm bảo gửi CSRF token trong header
    }
  })
  .then(response => {
    console.log('Check-in response status:', response.status);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Check-in response data:', data);
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Check-in';

    // Đóng modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('checkInModal'));
    if (modal) modal.hide();

    // Hiển thị thông báo
    Swal.fire({
      icon: data.success ? 'success' : 'error',
      title: data.success ? 'Check-in thành công' : 'Lỗi',
      text: data.message,
      confirmButtonText: 'OK',
      timer: data.success ? 3000 : null,
      timerProgressBar: data.success
    }).then(() => {
      // Cập nhật UI nếu cần
      if (data.success) {
        handleSuccessfulAttendance('checkin');
      }
    });
  })
  .catch(error => {
    console.error('Check-in error:', error);
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Check-in';

    // Đóng modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('checkInModal'));
    if (modal) modal.hide();

    // Hiển thị thông báo lỗi chi tiết
    Swal.fire({
      icon: 'error',
      title: 'Lỗi hệ thống',
      text: `Có lỗi xảy ra khi gửi yêu cầu: ${error.message}. Vui lòng thử lại.`,
      confirmButtonText: 'OK'
    });
  });
}

/**
 * Xử lý sự kiện click nút check-out
 */
function handleCheckOutClick() {
  console.log('handleCheckOutClick called');

  const checkOutForm = document.getElementById('checkOutForm');
  const submitBtn = document.getElementById('checkout_submit');
  const errorDiv = document.getElementById('checkout_error');

  if (!checkOutForm || !submitBtn) {
    console.error('Check-out form or submit button not found');
    return;
  }

  // Kiểm tra nếu nút đang bị disable để tránh click liên tục
  if (submitBtn.disabled) {
    console.log('Submit button is disabled, ignoring click');
    return;
  }

  // Lấy dữ liệu form
  const formData = new FormData(checkOutForm);

  // Kiểm tra dữ liệu
  const imageData = formData.get('checkout_image');
  const location = formData.get('checkout_location');

  console.log('Check-out data:', {
    'Has image': !!imageData,
    'Has location': !!location,
    'Image data length': imageData ? imageData.length : 0,
    'Location value': location || 'empty'
  });

  if (!imageData || !location) {
    errorDiv.textContent = 'Vui lòng chụp ảnh và cho phép truy cập vị trí';
    errorDiv.classList.remove('d-none');
    return;
  }

  // Disable nút và hiển thị loading
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Đang xử lý...';
  errorDiv.classList.add('d-none');

  // Gửi request
  const url = checkOutForm.getAttribute('action');
  console.log('Sending check-out request to:', url);

  // Thêm CSRF token vào FormData
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  formData.append('csrfmiddlewaretoken', csrfToken);

  fetch(url, {
    method: 'POST',
    body: formData,
    credentials: 'same-origin',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken // Đảm bảo gửi CSRF token trong header
    }
  })
  .then(response => {
    console.log('Check-out response status:', response.status);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Check-out response data:', data);
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Check-out';

    // Đóng modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('checkOutModal'));
    if (modal) modal.hide();

    // Hiển thị thông báo
    Swal.fire({
      icon: data.success ? 'success' : 'error',
      title: data.success ? 'Check-out thành công' : 'Lỗi',
      text: data.message,
      confirmButtonText: 'OK',
      timer: data.success ? 3000 : null,
      timerProgressBar: data.success
    }).then(() => {
      // Cập nhật UI nếu cần
      if (data.success) {
        handleSuccessfulAttendance('checkout');
      }
    });
  })
  .catch(error => {
    console.error('Check-out error:', error);
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Check-out';

    // Đóng modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('checkOutModal'));
    if (modal) modal.hide();

    // Hiển thị thông báo lỗi chi tiết
    Swal.fire({
      icon: 'error',
      title: 'Lỗi hệ thống',
      text: `Có lỗi xảy ra khi gửi yêu cầu: ${error.message}. Vui lòng thử lại.`,
      confirmButtonText: 'OK'
    });
  });
}
