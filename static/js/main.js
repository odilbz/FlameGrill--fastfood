// FlameGrill — main.js

// Add to cart
document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        const name = btn.dataset.name;
        const price = parseInt(btn.dataset.price);
        const emoji = btn.dataset.emoji;

        fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, name, price, emoji })
        })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Update cart count
                    const countEl = document.getElementById('cart-count');
                    if (countEl) countEl.textContent = data.cart_count;

                    // Animate button
                    btn.style.transform = 'scale(0.85)';
                    setTimeout(() => btn.style.transform = '', 200);

                    // Show toast
                    showToast('✅ ' + name + ' ajouté!');
                }
            });
    });
});

// Remove from cart
document.querySelectorAll('.remove-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        })
            .then(r => r.json())
            .then(data => {
                if (data.success) location.reload();
            });
    });
});

// Toast notification
function showToast(msg) {
    let toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
}
