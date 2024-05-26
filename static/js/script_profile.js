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

const logOutLink = document.querySelector('#logOutLink');

if (logOutLink != null) {
    logOutLink.addEventListener('click', () => {
        logout();
    });
}

async function logout() {
    const response = await fetch('/auth/logout', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
    });

    const data = await response.json();

    if (response.ok) {
        // Удаляем токен доступа из локального хранилища
        localStorage.removeItem('access_token');
        // Перенаправляем пользователя на главную страницу
        window.location.href = '/';
    } else {
        throw new Error(data.detail);
    }
}

const getMe = async () => {
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
                const new_data = await new_response.json();
                if (new_response.ok) {
                    return new_data;
                }
            }
            else {
                window.location.href = '/auth/login';
            }
        }
    } else if (response.redirected) {
        window.location.href = response.url;
    }
    const data = await response.json();
    return data;
};

const setProfileInfo = (data) => {
    if (data) {
        const userName = document.querySelector('#user-name');
        const userVerified = document.querySelector('#user-verified');
        const userEmail = document.querySelector('#user-email');
        userName.textContent = `Никнейм: ${data.username}`;
        if (data.is_verified) {
            userVerified.textContent = 'Статус учетной записи: подтвержденная';
        }
        else {
            userVerified.textContent = 'Статус учетной записи: не подтвержденная';
        }
        userEmail.textContent = `Email: ${data.email}`;
    }
};


getMe().then(setProfileInfo);
