window.onload = function () {
    const inputs = document.querySelectorAll('.input-container input');
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value.trim() !== '') {
            inputs[i].parentNode.classList.add('input-filled');
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.input-container input');

    inputs.forEach((input) => {
        input.addEventListener('input', () => {
            input.setAttribute('value', input.value);

            // проверяем, заполнено ли поле, и перемещаем label в соответствии с этим
            if (input.value) {
                input.nextElementSibling.classList.add('active');
            } else {
                input.nextElementSibling.classList.remove('active');
            }
        });
    });
});
