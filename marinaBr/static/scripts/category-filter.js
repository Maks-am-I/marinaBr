// Фильтрация товаров по категориям
document.addEventListener('DOMContentLoaded', function() {
    const categoryList = document.getElementById('list-categoties');
    const productList = document.getElementById('list-products');
    
    if (!categoryList || !productList) {
        return;
    }
    
    const categoryItems = categoryList.querySelectorAll('.category-filter');
    const productItems = productList.querySelectorAll('.item');
    
    // Функция фильтрации товаров
    function filterProducts(categoryId) {
        let visibleCount = 0;
        
        productItems.forEach(productItem => {
            const productCategoryId = productItem.getAttribute('context');
            
            if (categoryId === 'all' || productCategoryId === categoryId) {
                productItem.style.display = '';
                // Плавное появление
                productItem.style.opacity = '0';
                setTimeout(() => {
                    productItem.style.opacity = '1';
                }, 10);
                visibleCount++;
            } else {
                productItem.style.display = 'none';
            }
        });
        
        return visibleCount > 0;
    }
    
    // Обработчик клика на категорию
    categoryItems.forEach(categoryItem => {
        categoryItem.addEventListener('click', function() {
            const categoryId = this.id;
            const categoryText = this.textContent.trim();
            
            // Убрать активный класс у всех категорий
            categoryItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Добавить активный класс к выбранной категории
            this.classList.add('active');
            
            // Если это кнопка "Все", показываем все товары
            if (categoryText === 'Все') {
                filterProducts('all');
            } else {
                // Фильтровать товары по выбранной категории
                filterProducts(categoryId);
            }
        });
    });
    
    // По умолчанию показываем все товары
    // Ищем кнопку "Все" среди категорий
    let allButton = null;
    categoryItems.forEach(item => {
        if (item.textContent.trim() === 'Все') {
            allButton = item;
        }
    });
    
    if (allButton) {
        // Если есть кнопка "Все", активируем её и показываем все товары
        allButton.classList.add('active');
        filterProducts('all');
    } else if (categoryItems.length > 0) {
        // Если нет кнопки "Все", активируем первую категорию
        categoryItems[0].classList.add('active');
        filterProducts(categoryItems[0].id);
    } else {
        // Иначе показываем все товары
        filterProducts('all');
    }
});
