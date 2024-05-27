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

const registrationForm = document.querySelector('.registration-form');

if (registrationForm != null) {
    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.querySelector('#nickname').value;
        const email = document.querySelector('#login').value;
        const hashed_password = document.querySelector('#password').value;
        const confirm_hashed_password = document.querySelector('#confirm-password').value;

        if (hashed_password !== confirm_hashed_password) {
            alert('Пароли не совпадают');
            return;
        }

        const userData = {
            username,
            email,
            hashed_password
        };

        try {
            await registerUser(userData);
        } catch (error) {
            alert(error.message);
        }
    });
}


const loginForm = document.querySelector('.login-form');

if (loginForm != null) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.querySelector('#login').value;
        const password = document.querySelector('#password').value;

        const userData = {
            username,
            password
        };

        try {
            await loginUser(userData);
        } catch (error) {
            alert(error.message);
        }
    });
}

// Регистрация пользователя
async function registerUser(userData) {
    const response = await fetch('/auth/create', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    });

    const data = await response.json();

    if (response.ok) {
        // Сохраняем токен доступа в локальном хранилище
        localStorage.setItem('access_token', data.access_token);
        // Перенаправляем пользователя на главную страницу
        window.location.href = '/';
    } else {
        throw new Error(data.detail);
    }
}

async function loginUser(userData) {
    const response = await fetch('/auth/token', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(userData)
    });

    const data = await response.json();

    if (response.ok) {
        // Сохраняем токен доступа в локальном хранилище
        localStorage.setItem('access_token', data.access_token);
        // Перенаправляем пользователя на главную страницу
        window.location.href = '/';
    } else {
        throw new Error(data.detail);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

async function refreshToken() {
    const response = await fetch('/auth/refresh', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getCookie('refresh_token')}`
        },
    });
    const data = await response.json();
    if (response.ok) {
        // Сохраняем новый токен в localStorage
        localStorage.setItem('access_token', data.access_token);
        return data.access_token;
    }
}

let isAuthCheck = localStorage.getItem('isAuthCheck');

const checkAuth = async () => {
    isAuthCheck = (isAuthCheck === 'true');
    if (!isAuthCheck) {
        const response = await fetch('/users/me', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (!response.ok) {
            if (response.status === 401) {
                if (getCookie('refresh_token')) {
                    await refreshToken();
                    const new_access_token = localStorage.getItem('access_token');
                    const new_response = await fetch('/users/me', {
                        headers: {
                            'Authorization': `Bearer ${new_access_token}`
                        }
                    });
                }
                else {
                    localStorage.setItem('isAuthCheck', 'true');
                    window.location.href = '/auth/login';
                }
            }
        } else {
            window.location.href = '/';
        }
    }
};

// Проверяем текущий URL-адрес перед вызовом checkAuth
const currentUrl = window.location.href;
if (!currentUrl.includes('/annotation-video')) {
    checkAuth();
}


export { refreshToken, getCookie };
