document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('pet-tutor-select');
    const nameEl = document.getElementById('tutor-selected-name');
    const box = document.getElementById('tutor-selected-box');
    const form = document.getElementById('form-novo-pet');

    if (select && nameEl && box) {
        select.addEventListener('change', () => {
            if (select.value) {
                nameEl.textContent = select.value;
                box.classList.add('has-tutor');
            } else {
                nameEl.textContent = 'Nenhum tutor selecionado';
                box.classList.remove('has-tutor');
            }
        });
    }

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
});
