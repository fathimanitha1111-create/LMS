/**
 * Online LMS - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Auto-dismiss flash alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // 2. Initialize Bootstrap Tooltips
  const tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltips.map(function (el) {
    return new bootstrap.Tooltip(el);
  });

  // 3. AJAX Lesson Progress Toggle
  const toggleBtn = document.getElementById('btnToggleLessonComplete');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const lessonId = this.getAttribute('data-lesson-id');
      const url = `/lesson/${lessonId}/toggle/`;

      fetch(url, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const btnText = document.getElementById('lessonStatusText');
          const btnIcon = document.getElementById('lessonStatusIcon');
          const progressBar = document.getElementById('courseProgressBar');
          const progressText = document.getElementById('courseProgressText');

          if (data.completed) {
            toggleBtn.classList.remove('btn-outline-success');
            toggleBtn.classList.add('btn-success');
            if (btnIcon) btnIcon.className = 'bi bi-check-circle-fill me-2';
            if (btnText) btnText.textContent = 'Completed';
          } else {
            toggleBtn.classList.remove('btn-success');
            toggleBtn.classList.add('btn-outline-success');
            if (btnIcon) btnIcon.className = 'bi bi-circle me-2';
            if (btnText) btnText.textContent = 'Mark as Completed';
          }

          if (progressBar) {
            progressBar.style.width = data.progress_percentage + '%';
          }
          if (progressText) {
            progressText.textContent = data.progress_percentage + '%';
          }

          // Update sidebar checkmark
          const sideIcon = document.getElementById(`sideIcon-${lessonId}`);
          if (sideIcon) {
            sideIcon.className = data.completed ? 'bi bi-check-circle-fill text-success me-2' : 'bi bi-circle text-muted me-2';
          }
        }
      })
      .catch(err => console.error('Error toggling lesson:', err));
    });
  }
});
