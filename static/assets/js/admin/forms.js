// Xử lý AI Assistant cho trang Task Assignments
document.addEventListener('DOMContentLoaded', function() {
    // Kiểm tra xem có đang ở trang task assignments hay không
    if (document.getElementById('taskassignments_form')) {
        // Thêm button AI Assistant vào bên cạnh user select
        const userField = document.querySelector('.field-user .related-widget-wrapper');
        if (userField) {
            const aiButton = document.createElement('button');
            aiButton.type = 'button';
            aiButton.id = 'ai_suggest_user';
            aiButton.title = 'Đề xuất người dùng phù hợp bằng AI';
            aiButton.innerHTML = '<i class="bi bi-robot"></i> Đề xuất';
            aiButton.style.cssText = `
                background: #0d6efd !important;
                color: #ffffff !important;
                padding: 0.25rem 0.75rem !important;
                font-size: 0.875rem !important;
                line-height: 1.5 !important;
                border: 1px solid #0d6efd !important;
                border-radius: 0.25rem !important;
                margin-left: 0.5rem !important;
                margin-top: 0.25rem !important;
                width: auto !important;
                height: auto !important;
                transform: none !important;
                transition: none !important;
                overflow: hidden !important;
                position: relative !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                cursor: pointer !important;
            `;

            userField.appendChild(aiButton);
            
            // Tạo modal để hiển thị kết quả
            const modalHtml = `
            <div class="modal fade" id="aiSuggestionModal" tabindex="-1" aria-labelledby="aiSuggestionModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title" id="aiSuggestionModalLabel">
                                <i class="bi bi-robot me-2"></i>Đề xuất người dùng phù hợp
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div id="aiSuggestionLoading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Đang phân tích...</span>
                                </div>
                                <p class="mt-3">AI đang phân tích và đề xuất người dùng phù hợp...</p>
                            </div>
                            <div id="aiSuggestionContent" class="d-none">
                                <div class="mb-4">
                                    <div class="alert alert-primary">
                                        <h5 class="alert-heading">Đề xuất của AI:</h5>
                                        <div id="suggestedUserContainer" class="d-flex align-items-center">
                                            <span class="badge bg-primary me-2">Người dùng phù hợp nhất</span>
                                            <span id="suggestedUser" class="fw-bold fs-5"></span>
                                            <button id="applyUserSuggestion" class="btn btn-sm btn-success ms-auto">
                                                <i class="bi bi-check-lg"></i> Áp dụng
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="reasoning card">
                                    <div class="card-header bg-light">
                                        <h6 class="mb-0 fw-bold"><i class="bi bi-info-circle me-1"></i>Phân tích chi tiết</h6>
                                    </div>
                                    <div class="card-body">
                                        <div id="suggestionReasoning" class="reasoning-content"></div>
                                    </div>
                                </div>
                            </div>
                            <div id="aiSuggestionError" class="alert alert-danger d-none">
                                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                                <span id="errorMessage"></span>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                        </div>
                    </div>
                </div>
            </div>
            `;
            
            // Thêm modal vào DOM
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            // Tải thư viện Marked.js nếu chưa có
            if (!window.marked) {
                const markedScript = document.createElement('script');
                markedScript.src = '{% static "assets/js/marked.min.js" %}';
                document.head.appendChild(markedScript);
                
                // Đợi đến khi thư viện được load xong
                markedScript.onload = function() {
                    console.log('Marked.js đã được tải thành công');
                    marked.setOptions({
                        breaks: true,
                        gfm: true
                    });
                };
            }
            
            // Khởi tạo modal
            const aiSuggestionModal = new bootstrap.Modal(document.getElementById('aiSuggestionModal'));
            
            // Xử lý sự kiện click trên nút đề xuất AI
            aiButton.addEventListener('click', function() {
                const taskSelect = document.getElementById('id_task');
                const taskId = taskSelect.value;
                
                // Kiểm tra xem task đã được chọn chưa
                if (!taskId) {
                    alert('Vui lòng chọn Task trước khi sử dụng tính năng đề xuất.');
                    return;
                }
                
                // Reset modal state
                document.getElementById('aiSuggestionContent').classList.add('d-none');
                document.getElementById('aiSuggestionLoading').classList.remove('d-none');
                document.getElementById('aiSuggestionError').classList.add('d-none');
                
                // Hiển thị modal
                aiSuggestionModal.show();
                
                // Gọi API để lấy đề xuất
                fetch('/api/suggest-user-for-task/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        task_id: taskId
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Ẩn loading
                    document.getElementById('aiSuggestionLoading').classList.add('d-none');
                    
                    if (data.error) {
                        // Hiển thị lỗi
                        document.getElementById('errorMessage').textContent = data.error;
                        document.getElementById('aiSuggestionError').classList.remove('d-none');
                    } else {
                        // Hiển thị kết quả
                        document.getElementById('suggestedUser').textContent = data.suggested_user_name;
                        
                        // Sử dụng marked để render HTML nếu có thể
                        if (window.marked) {
                            // Trước tiên đảm bảo nội dung HTML không bị mất
                            const rawHtml = data.reasoning;
                            document.getElementById('suggestionReasoning').innerHTML = rawHtml;
                            
                            // Áp dụng các style cho các phần tử được render
                            const reasoningEl = document.getElementById('suggestionReasoning');
                            
                            // Tạo style cho các phần tử trong reasoning
                            reasoningEl.querySelectorAll('ul').forEach(ul => {
                                ul.classList.add('mb-0', 'ps-3');
                            });
                            
                            reasoningEl.querySelectorAll('li').forEach(li => {
                                li.classList.add('mb-2');
                            });
                            
                            reasoningEl.querySelectorAll('strong').forEach(strong => {
                                strong.classList.add('text-primary');
                            });
                        } else {
                            // Fallback nếu marked không có sẵn
                            document.getElementById('suggestionReasoning').innerHTML = data.reasoning;
                        }
                        
                        document.getElementById('aiSuggestionContent').classList.remove('d-none');
                        
                        // Xử lý nút áp dụng
                        document.getElementById('applyUserSuggestion').onclick = function() {
                            const userSelect = document.getElementById('id_user');
                            
                            // Tìm và chọn option chứa user được đề xuất
                            for (let i = 0; i < userSelect.options.length; i++) {
                                if (userSelect.options[i].value == data.suggested_user_id) {
                                    userSelect.selectedIndex = i;
                                    break;
                                }
                            }
                            
                            // Đóng modal
                            aiSuggestionModal.hide();
                        };
                    }
                })
                .catch(error => {
                    // Ẩn loading và hiển thị lỗi
                    console.error('Error:', error);
                    document.getElementById('aiSuggestionLoading').classList.add('d-none');
                    document.getElementById('errorMessage').textContent = `Không thể kết nối với máy chủ: ${error.message}`;
                    document.getElementById('aiSuggestionError').classList.remove('d-none');
                });
            });
        }
    }
});