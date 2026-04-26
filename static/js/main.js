function updateCartCount(count) {
    const badge = document.querySelector(".cart-count");
    if (badge) {
        badge.textContent = count;
        badge.style.transform = "scale(1.4)";
        setTimeout(() => badge.style.transform = "scale(1)", 300);
    }
}

function showToast(msg, color = "#2d6a4f") {
    let toast = document.querySelector(".toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.className = "toast";
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.background = color;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2500);
}

document.addEventListener("click", async (e) => {
    if (!e.target.classList.contains("add-btn")) return;
    const btn = e.target;
    const itemId = parseInt(btn.dataset.id);
    btn.textContent = "✓ Ajouté!";
    btn.classList.add("added");
    btn.disabled = true;
    try {
        const res = await fetch("/api/cart/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: itemId })
        });
        const data = await res.json();
        if (data.success) {
            updateCartCount(data.cart_count);
            showToast("✅ Ajouté au panier!");
        }
    } catch {
        showToast("❌ Erreur réseau", "#e63946");
    }
    setTimeout(() => {
        btn.textContent = "🛒 Ajouter";
        btn.classList.remove("added");
        btn.disabled = false;
    }, 2000);
});

document.addEventListener("click", async (e) => {
    if (!e.target.classList.contains("remove-btn")) return;
    const btn = e.target;
    const itemId = parseInt(btn.dataset.id);
    const card = btn.closest(".cart-item");
    card.style.opacity = "0.4";
    try {
        const res = await fetch("/api/cart/remove", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: itemId })
        });
        const data = await res.json();
        if (data.success) {
            card.remove();
            updateCartCount(data.cart_count);
            const totalEl = document.querySelector(".total-amount");
            if (totalEl) totalEl.textContent = data.total + " DA";
            showToast("🗑️ Article retiré", "#e63946");
            if (data.cart_count === 0) location.reload();
        }
    } catch {
        card.style.opacity = "1";
    }
});

const tabs = document.querySelectorAll(".tab-btn");
const cards = document.querySelectorAll(".menu-card");
tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const cat = tab.dataset.cat;
        cards.forEach(card => {
            card.style.display = (cat === "all" || card.dataset.category === cat) ? "flex" : "none";
        });
    });
});

const orderBtn = document.querySelector(".order-btn");
if (orderBtn) {
    orderBtn.addEventListener("click", async () => {
        orderBtn.textContent = "⏳ Traitement...";
        orderBtn.disabled = true;
        await new Promise(r => setTimeout(r, 1500));
        await fetch("/api/cart/clear", { method: "POST" });
        showToast("🎉 Commande confirmée! Merci!");
        setTimeout(() => { window.location.href = "/"; }, 2000);
    });
}