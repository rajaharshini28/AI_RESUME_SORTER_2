document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumes');
    const fileListPreview = document.getElementById('fileListPreview');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');

    if (dropZone && fileInput) {
        // Drag events
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, function(e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, function(e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        // Handle drop
        dropZone.addEventListener('drop', function(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            updateFileList(files);
        });

        // Handle file select
        fileInput.addEventListener('change', function() {
            updateFileList(this.files);
        });
    }

    function updateFileList(files) {
        if (!fileListPreview) return;
        fileListPreview.innerHTML = '';

        if (files.length === 0) return;

        Array.from(files).forEach((file, index) => {
            const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span>📄 <strong>${file.name}</strong> (${sizeMB} MB)</span>
                <span style="color: #34d399; font-weight: 600;">Ready</span>
            `;
            fileListPreview.appendChild(fileItem);
        });
    }

    if (uploadForm && submitBtn) {
        uploadForm.addEventListener('submit', function() {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '⚡ Processing & Embedding Resumes...';
        });
    }
});
