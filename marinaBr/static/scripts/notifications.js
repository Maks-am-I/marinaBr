// Закрытие уведомлений
document.addEventListener('DOMContentLoaded', function() {
    const messagesOverlay = document.getElementById('messages-overlay');
    
    if (!messagesOverlay) {
        return;
    }
    
    const notifications = messagesOverlay.querySelectorAll('.notification');
    const closeButtons = messagesOverlay.querySelectorAll('.notification__close');
    
    // Функция закрытия уведомления
    function closeNotification(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
            // Если все уведомления закрыты, удалить overlay
            if (messagesOverlay.querySelectorAll('.notification').length === 0) {
                messagesOverlay.remove();
            }
        }, 300);
    }
    
    // Закрытие по клику на крестик
    closeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const notification = this.closest('.notification');
            closeNotification(notification);
        });
    });
    
    // Закрытие по клику вне уведомления (на overlay)
    messagesOverlay.addEventListener('click', function(e) {
        // Проверяем, что клик был именно на overlay, а не на уведомлении
        if (e.target === messagesOverlay) {
            notifications.forEach(notification => {
                closeNotification(notification);
            });
        }
    });
    
    // Предотвращаем закрытие при клике на само уведомление
    notifications.forEach(notification => {
        notification.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});
