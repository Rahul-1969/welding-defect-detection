/**
 * WeldAI — Industrial Welding Defect Detection
 * Frontend Logic: upload, preview, inference, result display, nav
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {

    /* ------------------------------------------------------------------ */
    /* DOM References                                                        */
    /* ------------------------------------------------------------------ */
    const dropZone          = document.getElementById('dropZone');
    const imageInput        = document.getElementById('imageInput');
    const dropzoneContent   = document.getElementById('dropzoneContent');
    const previewContainer  = document.getElementById('previewContainer');
    const inputPreview      = document.getElementById('inputPreview');
    const fileNameEl        = document.getElementById('fileName');
    const fileSizeEl        = document.getElementById('fileSize');
    const fileDimensionsEl  = document.getElementById('fileDimensions');
    const btnRemoveImage    = document.getElementById('btnRemoveImage');

    const btnRun            = document.getElementById('btnRun');
    const btnRunText        = document.getElementById('btnRunText');
    const btnSpinner        = document.getElementById('btnSpinner');
    const btnClear          = document.getElementById('btnClear');
    const btnRunNew         = document.getElementById('btnRunNewInspection');

    const emptyState        = document.getElementById('emptyState');
    const loadingState      = document.getElementById('loadingState');
    const errorBanner       = document.getElementById('errorBanner');
    const errorMessage      = document.getElementById('errorMessage');
    const resultDisplay     = document.getElementById('resultDisplay');
    const resultImage       = document.getElementById('resultImage');

    const reportTimestamp   = document.getElementById('reportTimestamp');
    const statusBadge       = document.getElementById('statusBadge');
    const reportValStatus   = document.getElementById('reportValStatus');
    const rowConfidence     = document.getElementById('rowConfidence');
    const reportValConf     = document.getElementById('reportValConfidence');
    const rowDetections     = document.getElementById('rowDetections');
    const reportValDet      = document.getElementById('reportValDetections');
    const rowTime           = document.getElementById('rowTime');
    const reportValTime     = document.getElementById('reportValTime');

    /* ------------------------------------------------------------------ */
    /* State                                                                 */
    /* ------------------------------------------------------------------ */
    let currentFile = null;
    let objectUrl   = null;

    /* ------------------------------------------------------------------ */
    /* Helpers                                                               */
    /* ------------------------------------------------------------------ */
    function formatBytes(bytes, decimals = 1) {
        if (!bytes) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
    }

    function timestamp() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    /* ------------------------------------------------------------------ */
    /* Image Dimensions                                                      */
    /* ------------------------------------------------------------------ */
    inputPreview.addEventListener('load', () => {
        const { naturalWidth: w, naturalHeight: h } = inputPreview;
        fileDimensionsEl.textContent = (w && h) ? `${w} × ${h} px` : '';
    });

    /* ------------------------------------------------------------------ */
    /* File Selection                                                         */
    /* ------------------------------------------------------------------ */
    function handleFileSelect(file) {
        if (!file) return;

        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            showError('Unsupported file type. Please upload a JPG or PNG welding image.');
            return;
        }

        currentFile = file;

        if (objectUrl) URL.revokeObjectURL(objectUrl);
        objectUrl = URL.createObjectURL(file);

        inputPreview.src = objectUrl;
        fileNameEl.textContent = file.name;
        fileSizeEl.textContent = formatBytes(file.size);
        fileDimensionsEl.textContent = ''; // Will be set by the load event

        dropzoneContent.classList.add('hidden');
        previewContainer.classList.remove('hidden', 'animate-in');
        // Trigger reflow for animation restart
        void previewContainer.offsetWidth;
        previewContainer.classList.add('animate-in');

        btnRun.disabled = false;
        hideError();
    }

    /* ------------------------------------------------------------------ */
    /* Reset Helpers                                                          */
    /* ------------------------------------------------------------------ */
    function resetImage() {
        if (objectUrl) { URL.revokeObjectURL(objectUrl); objectUrl = null; }
        currentFile = null;
        imageInput.value = '';

        previewContainer.classList.add('hidden');
        previewContainer.classList.remove('animate-in');
        dropzoneContent.classList.remove('hidden');
        btnRun.disabled = true;
    }

    function resetResults() {
        emptyState.classList.remove('hidden');
        loadingState.classList.add('hidden');
        resultDisplay.classList.add('hidden');
        resultDisplay.classList.remove('animate-reveal');
        statusBadge.className = 'status-badge';
        statusBadge.textContent = '';
        hideError();
    }

    /* ------------------------------------------------------------------ */
    /* Error Display                                                          */
    /* ------------------------------------------------------------------ */
    function showError(msg) {
        errorMessage.textContent = msg || 'Please upload a valid welding image and try again.';
        errorBanner.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    function hideError() {
        errorBanner.classList.add('hidden');
    }

    /* ------------------------------------------------------------------ */
    /* Drag & Drop                                                            */
    /* ------------------------------------------------------------------ */
    dropZone.addEventListener('dragenter',  (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragover',   (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave',  (e) => { e.preventDefault(); dropZone.classList.remove('dragover'); });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const file = e.dataTransfer?.files[0];
        if (file) handleFileSelect(file);
    });

    // Keyboard accessibility for the dropzone
    dropZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); imageInput.click(); }
    });

    imageInput.addEventListener('change', (e) => {
        const file = e.target.files?.[0];
        if (file) handleFileSelect(file);
    });

    /* ------------------------------------------------------------------ */
    /* Button Events                                                          */
    /* ------------------------------------------------------------------ */
    btnRemoveImage.addEventListener('click', (e) => {
        e.stopPropagation();
        resetImage();
    });

    btnClear.addEventListener('click', () => {
        resetImage();
        resetResults();
    });

    if (btnRunNew) {
        btnRunNew.addEventListener('click', () => {
            resetImage();
            resetResults();
            dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    /* ------------------------------------------------------------------ */
    /* Run Inspection                                                         */
    /* ------------------------------------------------------------------ */
    btnRun.addEventListener('click', async () => {
        if (!currentFile) {
            showError('Please select an image before running inspection.');
            return;
        }

        // --- Transition to loading state ---
        btnRun.disabled = true;
        btnSpinner.classList.remove('hidden');
        btnRunText.textContent = 'Analyzing\u2026';

        emptyState.classList.add('hidden');
        resultDisplay.classList.add('hidden');
        resultDisplay.classList.remove('animate-reveal');
        statusBadge.className = 'status-badge';
        hideError();
        loadingState.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/detect', { method: 'POST', body: formData });

            let data = {};
            try { data = await response.json(); } catch (_) { /* empty body */ }

            if (!response.ok) {
                throw new Error(data.error || 'Server error — inspection could not be completed.');
            }
            if (data.error) {
                throw new Error(data.error);
            }

            // --- Populate result ---
            loadingState.classList.add('hidden');

            resultImage.src = data.image + '?t=' + Date.now();
            reportTimestamp.textContent = `Completed at ${timestamp()}`;

            const hasDefect = data.status === 'DEFECT DETECTED'
                           || (data.result && (data.result.includes('Bad') || data.result.includes('Defect')));

            if (hasDefect) {
                statusBadge.textContent   = 'DEFECT DETECTED';
                statusBadge.className     = 'status-badge badge-defect highlight-badge';
                reportValStatus.textContent = 'DEFECT DETECTED';
                reportValStatus.style.color = 'var(--status-defect-text)';
            } else {
                statusBadge.textContent   = 'NO DEFECT DETECTED';
                statusBadge.className     = 'status-badge badge-good highlight-badge';
                reportValStatus.textContent = 'NO DEFECT DETECTED';
                reportValStatus.style.color = 'var(--status-good-text)';
            }

            // Confidence — omit if 0 or absent
            if (data.confidence != null && data.confidence > 0) {
                reportValConf.textContent = (data.confidence * 100).toFixed(1) + '%';
                rowConfidence.classList.remove('hidden');
            } else {
                rowConfidence.classList.add('hidden');
            }

            // Detections count — always show (even 0)
            if (data.detections_count != null) {
                reportValDet.textContent = String(data.detections_count);
                rowDetections.classList.remove('hidden');
            } else {
                rowDetections.classList.add('hidden');
            }

            // Processing time
            if (data.processing_time != null) {
                reportValTime.textContent = data.processing_time + 's';
                rowTime.classList.remove('hidden');
            } else {
                rowTime.classList.add('hidden');
            }

            resultDisplay.classList.remove('hidden');
            void resultDisplay.offsetWidth;
            resultDisplay.classList.add('animate-reveal');

        } catch (err) {
            loadingState.classList.add('hidden');
            // Never expose raw error strings or stack traces to the user
            showError('Please upload a valid welding image and try again.');
        } finally {
            btnRun.disabled = false;
            btnSpinner.classList.add('hidden');
            btnRunText.textContent = 'Run Inspection';
        }
    });

    /* ------------------------------------------------------------------ */
    /* Navigation — scroll spy                                               */
    /* ------------------------------------------------------------------ */
    const allNavLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        const fromTop = window.scrollY + 80;
        allNavLinks.forEach(link => {
            const target = document.querySelector(link.getAttribute('href'));
            if (!target) return;
            const active = target.offsetTop <= fromTop &&
                           target.offsetTop + target.offsetHeight > fromTop;
            link.classList.toggle('active', active);
        });
        closeMobileNav();
    }, { passive: true });

    /* ------------------------------------------------------------------ */
    /* Mobile Hamburger                                                       */
    /* ------------------------------------------------------------------ */
    const navHamburger = document.getElementById('navHamburger');
    const navLinksEl   = document.getElementById('navLinks');
    const hamOpen      = navHamburger?.querySelector('.ham-open');
    const hamClose     = navHamburger?.querySelector('.ham-close');

    function closeMobileNav() {
        if (!navLinksEl) return;
        navLinksEl.classList.remove('mobile-open');
        navHamburger?.setAttribute('aria-expanded', 'false');
        hamOpen?.classList.remove('hidden');
        hamClose?.classList.add('hidden');
    }

    navHamburger?.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = navLinksEl.classList.contains('mobile-open');
        if (isOpen) {
            closeMobileNav();
        } else {
            navLinksEl.classList.add('mobile-open');
            navHamburger.setAttribute('aria-expanded', 'true');
            hamOpen?.classList.add('hidden');
            hamClose?.classList.remove('hidden');
        }
    });

    // Close on link click
    allNavLinks.forEach(link => link.addEventListener('click', closeMobileNav));

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (navLinksEl?.classList.contains('mobile-open') &&
            !navLinksEl.contains(e.target) &&
            !navHamburger?.contains(e.target)) {
            closeMobileNav();
        }
    });

    /* ------------------------------------------------------------------ */
    /* Reduced Motion Respect                                                */
    /* ------------------------------------------------------------------ */
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
        document.documentElement.classList.add('no-motion');
    }

});