document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('delete-modal');
    const form = document.getElementById('delete-modal-form');
    const nameEl = document.getElementById('delete-modal-name');
    const typeEl = document.getElementById('delete-modal-type-label');
    const passwordInput = document.getElementById('delete-modal-password');
    const nextInput = document.getElementById('delete-modal-next');
    const closeBtn = document.getElementById('delete-modal-close');
    const cancelBtn = document.getElementById('delete-modal-cancel');

    if (!modal || !form) return;

    function openModal(btn) {
        form.action = btn.dataset.deleteUrl;
        nameEl.textContent = btn.dataset.deleteName;
        typeEl.textContent = btn.dataset.deleteType === 'pet' ? 'pet' : 'tutor';
        nextInput.value = window.location.pathname + window.location.search;
        passwordInput.value = '';
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('modal-open');
        passwordInput.focus();
    }

    function closeModal() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
        passwordInput.value = '';
    }

    document.querySelectorAll('.btn-open-delete').forEach((btn) => {
        btn.addEventListener('click', () => openModal(btn));
    });

    closeBtn?.addEventListener('click', closeModal);
    cancelBtn?.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
});
