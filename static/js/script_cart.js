// Массив для хранения датасетов в корзине
let cart = [];

// Функция для добавления датасета в корзину
function addToCart(dataset) {
    // Ограничение на количество датасетов в корзине
    if (cart.length >= 10) {
        alert("Максимальное количество датасетов в корзине - 10");
        return;
    }

    // Добавляем датасет в корзину
    cart.push(dataset);

    // сохраняем корзину в localStorage
    saveCartToLocalStorage();

    // Обновляем корзину
    updateCart();
}

// Функция для удаления датасета из корзины
function removeFromCart(index) {
    // Удаляем датасет из корзины
    cart.splice(index, 1);
    saveCartToLocalStorage(); // сохраняем корзину в localStorage
    updateCart();
}

// Функция для обновления корзины
function updateCart() {
    // Обнуляем корзину
    let cartContainer = document.querySelector(".datasets-cart");
    cartContainer.innerHTML = "";

    // Перебираем датасеты в корзине и добавляем их в корзину на страницу
    cart.forEach((dataset, index) => {
        cartContainer.innerHTML += `
      <div class="dataset-cart">
        <div class="img-cart-container"><img src="${dataset.image}" alt="${dataset.name}"></div>
        <div class="cart-info-container">
          <h3>Название датасета: ${dataset.name}</h3>
          <p>Цена: ${dataset.price}$</p>
          <button class="remove-btn-cart" onclick="removeFromCart(${index})">Удалить из корзины</button>
        </div>
      </div>
    `;
    });

    // Обновляем количество и общую сумму в корзине
    let quantity = document.querySelector("#quantity");
    let totalPrice = document.querySelector("#total-price");
    quantity.textContent = cart.length;
    totalPrice.textContent = cart.reduce((acc, dataset) => acc + dataset.price, 0) + "$";
}

// Функция для отправки заказа на бэкенд
function sendOrder() {
    // Отправляем заказ на бэкенд, например, с помощью fetch API
    fetch("/api/orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(cart),
    })
        .then((response) => response.json())
        .then((data) => {
            // Обрабатываем ответ от бэкенда
            console.log(data);

            // Обнуляем корзину
            cart = [];
            updateCart();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

// Функция для проверки истечения срока хранения корзины в localStorage
function isCartExpired() {
    let cartExpiration = localStorage.getItem("cartExpiration");
    if (!cartExpiration) {
        return true;
    }
    let currentTime = new Date().getTime();
    if (currentTime > parseInt(cartExpiration)) {
        return true;
    }
    return false;
}

// Функция для загрузки корзины из localStorage
function loadCartFromLocalStorage() {
    if (isCartExpired()) {
        cart = [];
        return;
    }
    let cartData = localStorage.getItem("cart");
    if (cartData) {
        cart = JSON.parse(cartData);
    } else {
        cart = [];
    }
    updateCart();
}

// Функция для сохранения корзины в localStorage
function saveCartToLocalStorage() {
    localStorage.setItem("cart", JSON.stringify(cart));
    let expirationTime = new Date().getTime() + 30 * 24 * 60 * 60 * 1000; // 30 дней в миллисекундах
    localStorage.setItem("cartExpiration", expirationTime);
}

// Загружаем корзину из localStorage при загрузке страницы
loadCartFromLocalStorage();

// Навешиваем обработчик события click на кнопки "Добавить в корзину"
let addToCartBtns = document.querySelectorAll(".add-to-cart-btn");
addToCartBtns.forEach((btn) => {
    btn.addEventListener("click", (event) => {
        event.preventDefault(); // Отменяем стандартное действие ссылки

        // Получаем id датасета из атрибута data-dataset-id
        let datasetId = event.target.dataset.datasetId;

        // Отправляем запрос на бэк для получения данных о датасете
        fetch(`/company/datasets/${datasetId}`)
            .then((response) => response.json())
            .then((data) => {
                // Создаем объект датасета
                let dataset = {
                    id: data.id,
                    name: data.name,
                    description: data.description,
                    imageCount: data.imageCount,
                    categories: data.categories,
                    format: data.format,
                    size: data.size,
                    price: parseFloat(data.price),
                    image: `/static/images/${data.image}`
                };

                // Добавляем датасет в корзину
                addToCart(dataset);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    });
});

// Навешиваем обработчик события на кнопку "Удалить из корзины"
const removeBtns = document.querySelectorAll('.remove-btn-cart');
removeBtns.forEach(btn => {
    btn.addEventListener('click', function (event) {
        // Предотвращаем стандартное поведение браузера
        event.preventDefault();

        // Находим родительский элемент .dataset-cart
        const datasetCart = event.target.closest('.dataset-cart');

        // Удаляем элемент .dataset-cart из корзины
        datasetCart.remove();

        // Обновляем количество и общую стоимость товаров в корзине
        const quantity = document.querySelector('#quantity');
        const totalPrice = document.querySelector('#total-price');
        const datasets = document.querySelectorAll('.dataset-cart');
        quantity.textContent = datasets.length;
        let total = 0;
        datasets.forEach(dataset => {
            const price = parseFloat(dataset.querySelector('.cart-info-container p:nth-child(2)').textContent.replace('$', ''));
            total += price;
        });
        totalPrice.textContent = total.toFixed(2) + '$';
    });
});
