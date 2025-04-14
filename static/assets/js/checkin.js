document.addEventListener('DOMContentLoaded', function() {
    // Hàm hiển thị lỗi
    function showError(errorDivId, message) {
      const errorDiv = document.getElementById(errorDivId);
      if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
        setTimeout(() => errorDiv.classList.add('d-none'), 5000);
      }
    }
  
    // Hàm khởi tạo webcam
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
  
      if (!modal || !video || !canvas || !snapButton || !imageDataInput || !previewImg || !submitButton || !loading) {
        console.error('Một hoặc nhiều phần tử không tồn tại trong setupWebcam:', { modalId, videoId, canvasId, snapButtonId, imageDataId, previewId, submitButtonId, loadingId });
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
            showError(modalId + '_error', 'Không thể truy cập webcam: ' + err.message);
          });
      });
  
      modal.addEventListener('hidden.bs.modal', () => {
        if (stream) {
          stream.getTracks().forEach(track => track.stop());
          stream = null;
        }
        video.srcObject = null;
        previewImg.classList.add('d-none');
        imageDataInput.value = '';
        snapButton.classList.remove('btn-success');
        snapButton.classList.add('btn-secondary');
        submitButton.disabled = true;
      });
  
      snapButton.addEventListener('click', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7);
        imageDataInput.value = compressedDataUrl;
        previewImg.src = compressedDataUrl;
        previewImg.classList.remove('d-none');
        
        snapButton.classList.remove('btn-secondary');
        snapButton.classList.add('btn-success');
        const locationInput = document.getElementById(modalId === 'checkInModal' ? 'checkin_location' : 'checkout_location');
        submitButton.disabled = !imageDataInput.value || !locationInput?.value;
      });
    }
  
    // Hàm lấy vị trí
    function setupGeolocation(modalId, inputId, loadingId) {
      const modal = document.getElementById(modalId);
      const input = document.getElementById(inputId);
      const loading = document.getElementById(loadingId);
      const submitButton = document.getElementById(modalId + '_submit');
  
      if (!modal || !input || !loading || !submitButton) {
        console.error('Một hoặc nhiều phần tử không tồn tại trong setupGeolocation:', { modalId, inputId, loadingId });
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
  
    // Khởi tạo check-in
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
  
    // Khởi tạo check-out
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
  });