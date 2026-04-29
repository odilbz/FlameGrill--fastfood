document.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        }).then(r => r.json()).then(data => {
            if (data.success) {
                const el = document.getElementById('cart-count');
                if (el) el.textContent = data.cart_count;
                btn.style.transform = 'scale(0.8)';
                setTimeout(() => btn.style.transform = '', 200);
                showToast('✅ ' + btn.dataset.name + ' ajouté!');
            }
        });
    });
});

document.querySelectorAll('.rm-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: parseInt(btn.dataset.id) })
        }).then(() => location.reload());
    });
});

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}
