(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation-principale');
  const dropdowns = [...document.querySelectorAll('.nav-dropdown')];

  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    navigation.classList.toggle('is-open', open);
    if (!open) dropdowns.forEach(dropdown => { dropdown.open = false; });
  }

  menuButton.addEventListener('click', () => {
    setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
  });

  dropdowns.forEach(dropdown => {
    dropdown.addEventListener('toggle', () => {
      if (dropdown.open) dropdowns.forEach(other => { if (other !== dropdown) other.open = false; });
    });
  });

  document.addEventListener('click', event => {
    dropdowns.forEach(dropdown => {
      if (!dropdown.contains(event.target)) dropdown.open = false;
    });
    if (navigation.classList.contains('is-open') && !navigation.contains(event.target) && !menuButton.contains(event.target)) {
      setMenu(false);
    }
  });

  navigation.addEventListener('click', event => {
    if (event.target.closest('a') && window.matchMedia('(max-width: 760px)').matches) setMenu(false);
  });

  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const openDropdown = dropdowns.find(dropdown => dropdown.open);
    if (openDropdown) {
      openDropdown.open = false;
      openDropdown.querySelector('summary').focus();
    } else if (navigation.classList.contains('is-open')) {
      setMenu(false);
      menuButton.focus();
    }
  });

  window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
    if (event.matches) setMenu(false);
  });
})();
