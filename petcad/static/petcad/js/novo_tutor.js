document.addEventListener('DOMContentLoaded', () => {
    const cpfInput = document.getElementById('tutor-cpf');
    const telInput = document.getElementById('tutor-telefone');
    const cepInput = document.getElementById('tutor-cep');
    const form = document.getElementById('form-novo-tutor');

    if (cpfInput) {
        cpfInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    }

    if (telInput) {
        telInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);

            if (value.length > 10) {
                value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
            } else if (value.length > 0) {
                value = value.replace(/^(\d*)/, '($1');
            }

            e.target.value = value;
        });
    }

    if (cepInput) {
        cepInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) value = value.slice(0, 8);
            if (value.length > 5) {
                value = value.replace(/^(\d{5})(\d{1,3})/, '$1-$2');
            }
            e.target.value = value;

            if (value.replace(/\D/g, '').length === 8) {
                fetchAddress(value.replace(/\D/g, ''));
            }
        });

        cepInput.addEventListener('blur', () => {
            const digits = cepInput.value.replace(/\D/g, '');
            if (digits.length === 8) {
                fetchAddress(digits);
            }
        });
    }

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
});

async function fetchAddress(cep) {
    const logradouro = document.getElementById('tutor-logradouro');
    const complemento = document.getElementById('tutor-complemento');
    const bairro = document.getElementById('tutor-bairro');
    const cidade = document.getElementById('tutor-cidade');
    const estado = document.getElementById('tutor-estado');

    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();

        if (data.erro) return;

        if (logradouro) logradouro.value = data.logradouro || '';
        if (complemento) complemento.value = data.complemento || '';
        if (bairro) bairro.value = data.bairro || '';
        if (cidade) cidade.value = data.localidade || '';
        if (estado) estado.value = data.uf || '';
    } catch (error) {
        return;
    }
}
