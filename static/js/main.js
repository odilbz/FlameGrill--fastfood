document.addEventListener('DOMContentLoaded', function () {

    // ADD TO CART
    document.querySelectorAll('.add-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = parseInt(this.dataset.id);
            const name = this.dataset.name || '';
            fetch('/api/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id })
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        const el = document.getElementById('cart-count');
                        if (el) el.textContent = data.cart_count;
                        showToast('✅ ' + name + ' ajouté!');
                    }
                })
                .catch(err => console.error('Cart error:', err));
        });
    });

    // REMOVE FROM CART
    document.querySelectorAll('.rm-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            fetch('/api/cart/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: parseInt(this.dataset.id) })
            }).then(() => location.reload());
        });
    });

});

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}
