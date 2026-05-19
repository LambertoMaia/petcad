document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('pet-tutor-select');
    const nameEl = document.getElementById('tutor-selected-name');
    const box = document.getElementById('tutor-selected-box');

    function updateTutorDisplay() {
        if (!select || !nameEl || !box) return;

        const option = select.options[select.selectedIndex];
        const label = option.textContent.trim();
        if (select.value && label && !option.disabled) {
            nameEl.textContent = label;
            box.classList.add('has-tutor');
        } else {
            nameEl.textContent = 'Nenhum tutor selecionado';
            box.classList.remove('has-tutor');
        }
    }

    if (select) {
        select.addEventListener('change', updateTutorDisplay);
        updateTutorDisplay();
    }
});
