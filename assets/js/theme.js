(function () {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');

  function syncToggle() {
    if (!toggle) return;
    const dark = root.dataset.theme === 'dark';
    const label = dark ? 'Switch to light mode' : 'Switch to dark mode';
    toggle.setAttribute('aria-label', label);
    toggle.title = label;
  }

  if (toggle) {
    syncToggle();
    toggle.addEventListener('click', function () {
      const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = theme;
      try { localStorage.setItem('theme', theme); } catch (error) { /* Storage may be unavailable. */ }
      syncToggle();
    });
  }

  const emailLink = document.querySelector('.email-link');
  const copyStatus = document.querySelector('.email-copy-status');
  if (!emailLink || !copyStatus) return;

  let statusTimer;

  async function copyEmail(address) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(address);
        return true;
      } catch (error) { /* Fall back for browsers without clipboard permission. */ }
    }

    const field = document.createElement('textarea');
    field.value = address;
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.appendChild(field);
    field.select();
    let copied = false;
    try { copied = document.execCommand('copy'); } catch (error) { /* Leave the mail link usable. */ }
    field.remove();
    return copied;
  }

  emailLink.addEventListener('click', async function (event) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const address = emailLink.href.slice('mailto:'.length);
    const copied = await copyEmail(address);
    if (copied) {
      copyStatus.textContent = 'Copied!';
      clearTimeout(statusTimer);
      statusTimer = setTimeout(function () { copyStatus.textContent = ''; }, 2500);
    }
    setTimeout(function () { window.location.href = emailLink.href; }, copied ? 900 : 0);
  });
})();
