// ── Live Search ───────────────────────────────────────────────────────────────
const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');

if (searchInput) {
  let debounceTimer;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      searchDropdown.classList.remove('open');
      searchDropdown.innerHTML = '';
      return;
    }
    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (data.length === 0) {
          searchDropdown.classList.remove('open');
          return;
        }
        searchDropdown.innerHTML = data.map(p =>
          `<div class="search-result-item" onclick="location.href='/product/${p.id}'">
            <span>${p.name}</span>
            <span style="color:var(--muted);font-size:.8rem">$${p.price.toFixed(2)}</span>
          </div>`
        ).join('');
        searchDropdown.classList.add('open');
      } catch(e) {}
    }, 280);
  });

  document.addEventListener('click', e => {
    if (!searchInput.contains(e.target)) {
      searchDropdown.classList.remove('open');
    }
  });

  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && searchInput.value.trim()) {
      window.location.href = `/products?q=${encodeURIComponent(searchInput.value.trim())}`;
    }
  });
}

// ── Auto-dismiss flash messages ───────────────────────────────────────────────
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .4s ease, transform .4s ease';
    el.style.opacity = '0';
    el.style.transform = 'translateX(20px)';
    setTimeout(() => el.remove(), 400);
  }, 3500);
});

// ── Animate product cards on scroll ──────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.product-card').forEach((card, i) => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(24px)';
  card.style.transition = `opacity .4s ease ${i * 0.06}s, transform .4s ease ${i * 0.06}s, box-shadow .2s ease, transform .2s ease`;
  observer.observe(card);
});
