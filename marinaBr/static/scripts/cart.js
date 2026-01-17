// Получить CSRF токен
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Обновить счетчик корзины в header
function updateCartBadge(count) {
    const cartBadge = document.querySelector('.cart-badge');
    const cartLink = document.querySelector('.header__cart a');
    
    if (count > 0) {
        if (!cartBadge) {
            const badge = document.createElement('span');
            badge.className = 'cart-badge';
            badge.textContent = count;
            cartLink.appendChild(badge);
        } else {
            cartBadge.textContent = count;
        }
    } else {
        if (cartBadge) {
            cartBadge.remove();
        }
    }
}

// Добавить товар в корзину
function addToCart(productId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при добавлении товара', 'error');
    });
}

// Добавить готовое решение в корзину
function addReadySolutionToCart(solutionId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/add-solution/${solutionId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при добавлении готового решения', 'error');
    });
}

// Удалить готовое решение из корзины
function removeReadySolutionFromCart(solutionId) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/remove-solution/${solutionId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
            // Удалить элемент из DOM
            const cartItem = document.querySelector(`.cart-item[data-ready-solution-id="${solutionId}"]`);
            if (cartItem) {
                cartItem.remove();
                // Обновить общую сумму
                updateTotalPrice(data.total_price);
                // Проверить, пуста ли корзина
                checkEmptyCart();
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при удалении готового решения', 'error');
    });
}

// Обновить количество готового решения
function updateReadySolutionCartItem(solutionId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/update-solution/${solutionId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
            // Обновить отображение количества
            const quantityDisplay = document.querySelector(`.cart-item[data-ready-solution-id="${solutionId}"] .quantity-display`);
            if (quantityDisplay) {
                quantityDisplay.textContent = quantity;
            }
            // Обновить общую сумму
            updateTotalPrice(data.total_price);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при обновлении количества', 'error');
    });
}

// Удалить товар из корзины
function removeFromCart(productId) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/remove/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
            // Удалить элемент из DOM
            const cartItem = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
            if (cartItem) {
                cartItem.remove();
                // Обновить общую сумму
                updateTotalPrice(data.total_price);
                // Проверить, пуста ли корзина
                checkEmptyCart();
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при удалении товара', 'error');
    });
}

// Обновить количество товара
function updateCartItem(productId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrftoken);

    fetch(`/cart/update/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_total);
            // Обновить отображение количества
            const quantityDisplay = document.querySelector(`.cart-item[data-product-id="${productId}"] .quantity-display`);
            if (quantityDisplay) {
                quantityDisplay.textContent = quantity;
            }
            // Обновить сумму товара
            const itemTotal = document.querySelector(`.cart-item[data-product-id="${productId}"] .item-total`);
            if (itemTotal) {
                itemTotal.textContent = data.item_total + ' ₽';
            }
            // Обновить общую сумму
            updateTotalPrice(data.total_price);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при обновлении количества', 'error');
    });
}

// Обновить общую сумму
function updateTotalPrice(totalPrice) {
    const totalPriceElement = document.getElementById('cart-total-price');
    const totalPriceBottom = document.getElementById('cart-total-price-bottom');
    if (totalPriceElement) {
        totalPriceElement.textContent = totalPrice + ' ₽';
    }
    if (totalPriceBottom) {
        totalPriceBottom.textContent = totalPrice + ' ₽';
    }
}

// Проверить, пуста ли корзина
function checkEmptyCart() {
    const cartItems = document.querySelectorAll('.cart-item');
    if (cartItems.length === 0) {
        // Перезагрузить страницу для показа пустой корзины
        window.location.reload();
    }
}

// Показать уведомление
function showNotification(message, type = 'success') {
    // Создать элемент уведомления
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Показать уведомление
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Скрыть и удалить через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Обработчики для главной страницы
document.addEventListener('DOMContentLoaded', function() {
    // Кнопки "В корзину" для обычных продуктов
    const addToCartButtons = document.querySelectorAll('.button-to-card:not(.button-ready-solution)');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const item = this.closest('.item');
            const quantityInput = item.querySelector('.item-quantity');
            const quantity = quantityInput ? parseInt(quantityInput.textContent) : 1;
            
            if (productId) {
                addToCart(productId, quantity);
            }
        });
    });
    
    // Кнопки "В корзину" для готовых решений
    const addReadySolutionButtons = document.querySelectorAll('.button-ready-solution');
    addReadySolutionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const solutionId = this.getAttribute('data-ready-solution-id');
            const bundleItem = this.closest('.bundle-item');
            const quantityInput = bundleItem.querySelector('.item-quantity');
            const quantity = quantityInput ? parseInt(quantityInput.textContent) : 1;
            
            if (solutionId) {
                addReadySolutionToCart(solutionId, quantity);
            }
        });
    });
    
    // Кнопки увеличения/уменьшения количества на главной странице
    const increaseButtons = document.querySelectorAll('.increase-qty');
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const config = this.closest('.button-config');
            const quantitySpan = config.querySelector('.item-quantity');
            if (quantitySpan) {
                let quantity = parseInt(quantitySpan.textContent);
                quantity++;
                quantitySpan.textContent = quantity;
            }
        });
    });
    
    const decreaseButtons = document.querySelectorAll('.decrease-qty');
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const config = this.closest('.button-config');
            const quantitySpan = config.querySelector('.item-quantity');
            if (quantitySpan) {
                let quantity = parseInt(quantitySpan.textContent);
                if (quantity > 1) {
                    quantity--;
                    quantitySpan.textContent = quantity;
                }
            }
        });
    });
});

// Обработчики для страницы корзины
document.addEventListener('DOMContentLoaded', function() {
    // Кнопки увеличения количества
    const increaseButtons = document.querySelectorAll('.increase-btn');
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const quantitySpan = this.parentElement.querySelector('.quantity-display');
            let quantity = parseInt(quantitySpan.textContent);
            quantity++;
            updateCartItem(productId, quantity);
        });
    });
    
    // Кнопки уменьшения количества
    const decreaseButtons = document.querySelectorAll('.decrease-btn');
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const quantitySpan = this.parentElement.querySelector('.quantity-display');
            let quantity = parseInt(quantitySpan.textContent);
            if (quantity > 1) {
                quantity--;
                updateCartItem(productId, quantity);
            }
        });
    });
    
    // Кнопки увеличения количества для готовых решений
    const increaseSolutionButtons = document.querySelectorAll('.increase-btn-solution');
    increaseSolutionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const solutionId = this.getAttribute('data-ready-solution-id');
            const quantitySpan = this.parentElement.querySelector('.quantity-display');
            let quantity = parseInt(quantitySpan.textContent);
            quantity++;
            updateReadySolutionCartItem(solutionId, quantity);
        });
    });
    
    // Кнопки уменьшения количества для готовых решений
    const decreaseSolutionButtons = document.querySelectorAll('.decrease-btn-solution');
    decreaseSolutionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const solutionId = this.getAttribute('data-ready-solution-id');
            const quantitySpan = this.parentElement.querySelector('.quantity-display');
            let quantity = parseInt(quantitySpan.textContent);
            if (quantity > 1) {
                quantity--;
                updateReadySolutionCartItem(solutionId, quantity);
            }
        });
    });
    
    // Кнопки удаления для продуктов
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            if (confirm('Удалить товар из корзины?')) {
                removeFromCart(productId);
            }
        });
    });
    
    // Кнопки удаления для готовых решений
    const removeSolutionButtons = document.querySelectorAll('.remove-btn-solution');
    removeSolutionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const solutionId = this.getAttribute('data-ready-solution-id');
            if (confirm('Удалить готовое решение из корзины?')) {
                removeReadySolutionFromCart(solutionId);
            }
        });
    });
    
    // Кнопка оформления заказа
    const orderBtn = document.getElementById('order-btn');
    if (orderBtn) {
        orderBtn.addEventListener('click', function() {
            // Пока просто показываем сообщение
            // В будущем можно добавить форму оформления заказа
            alert('Для оформления заказа свяжитесь с нами по телефону +7(953)596-55-20 или через форму обратной связи на главной странице.');
        });
    }
});
