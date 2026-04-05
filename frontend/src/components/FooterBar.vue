<template>
  <footer class="footer">
    <div class="container footer-inner">
      <p class="footer-brand">◆ ShopVue</p>
      <p class="footer-text">A learning project built with Vue.js & Python Flask</p>
      <p class="footer-text">© 2026 — Built with care for beginners everywhere</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--color-border-light);
  padding: var(--space-xl) 0;
  margin-top: auto;
}

.footer-inner {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.footer-brand {
  font-family: var(--font-heading);
  font-weight: 700;
  color: var(--color-text);
}

.footer-text {
  font-size: 0.8rem;
  color: var(--color-text-light);
}
</style>
