(() => {
  'use strict';

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation-principale');
  const dropdowns = [...document.querySelectorAll('.nav-dropdown')];

  function setMenu(open) {
    if (!menuButton || !navigation) return;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    navigation.classList.toggle('is-open', open);
    if (!open) dropdowns.forEach(dropdown => { dropdown.open = false; });
  }

  if (menuButton && navigation) {
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
  }

  function normalise(value) {
    return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fr').trim();
  }

  function setupSearch(formSelector, itemSelector, countSelector, emptySelector, inputSelector, initialQuery) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    const input = form.querySelector(inputSelector);
    const items = [...document.querySelectorAll(itemSelector)];
    const count = document.querySelector(countSelector);
    const empty = document.querySelector(emptySelector);
    if (!input || !count || !empty) return;
    const submit = form.querySelector('button[type=submit]');
    if (submit) submit.disabled = false;
    if (initialQuery) input.value = initialQuery;

    function filter() {
      const words = normalise(input.value).split(/\s+/).filter(Boolean);
      let visible = 0;
      items.forEach(item => {
        const haystack = normalise(item.dataset.search || item.textContent);
        const matches = words.every(word => haystack.includes(word));
        item.hidden = !matches;
        if (matches) visible += 1;
      });
      count.textContent = `${visible} résultat${visible === 1 ? '' : 's'}`;
      empty.hidden = visible !== 0;
    }

    form.addEventListener('submit', event => { event.preventDefault(); filter(); });
    input.addEventListener('input', filter);
    filter();
  }

  setupSearch('[data-catalog-search]', '[data-search-item]', '[data-result-count]', '[data-no-results]', 'input', new URLSearchParams(location.search).get('q'));
  setupSearch('[data-agency-search]', '[data-agency-item]', '[data-agency-count]', '[data-agency-empty]', 'input');

  const quoteForm = document.querySelector('[data-quote-form]');
  if (quoteForm) {
    const panels = [...quoteForm.querySelectorAll('[data-quote-step]')];
    const steps = [...document.querySelectorAll('.step-list li')];
    const activity = quoteForm.querySelector('[name="activity"]');
    const size = quoteForm.querySelector('[name="size"]');
    const needs = [...quoteForm.querySelectorAll('[name="need"]')];
    let current = 1;

    quoteForm.querySelectorAll('button[disabled]').forEach(button => { button.disabled = false; });
    // The official product codes only preselect local topics; they never initiate a real request.
    const presets = {
      ACT5: 'Locaux, matériel et multirisque',
      ACT2: 'Véhicules professionnels',
      PS1: 'Santé des salariés',
      ACT4: 'Responsabilité civile professionnelle'
    };
    const preset = presets[new URLSearchParams(location.search).get('product')];
    const presetCheckbox = needs.find(input => input.value === preset);
    if (presetCheckbox) presetCheckbox.checked = true;

    function selectedNeeds() {
      return needs.filter(input => input.checked).map(input => input.value);
    }

    function summaryValues() {
      return [
        ['Activité', activity.value],
        ['Taille de la structure', size.value],
        ['Besoins sélectionnés', selectedNeeds().join(', ')]
      ];
    }

    function updateSummary() {
      quoteForm.querySelectorAll('[data-quote-summary]').forEach(list => {
        list.replaceChildren();
        summaryValues().forEach(([label, value]) => {
          const row = document.createElement('div');
          const term = document.createElement('dt');
          const description = document.createElement('dd');
          term.textContent = label;
          description.textContent = value;
          row.append(term, description);
          list.append(row);
        });
      });
    }

    function showStep(number) {
      current = number;
      if (current >= 3) updateSummary();
      panels.forEach(panel => { panel.hidden = Number(panel.dataset.quoteStep) !== current; });
      steps.forEach((step, index) => {
        if (index + 1 === current) step.setAttribute('aria-current', 'step');
        else step.removeAttribute('aria-current');
        step.classList.toggle('is-complete', index + 1 < current);
      });
      const heading = panels[current - 1].querySelector('h2');
      if (heading) heading.focus();
    }

    function clearError(step) {
      const error = quoteForm.querySelector(`[data-step-error="${step}"]`);
      if (error) { error.hidden = true; error.textContent = ''; }
    }

    function validateStep() {
      clearError(current);
      if (current === 1 && (!activity.value || !size.value)) {
        const error = quoteForm.querySelector('[data-step-error="1"]');
        error.textContent = 'Sélectionnez une activité et une taille de structure pour continuer.';
        error.hidden = false;
        (!activity.value ? activity : size).focus();
        return false;
      }
      if (current === 2 && !selectedNeeds().length) {
        const error = quoteForm.querySelector('[data-step-error="2"]');
        error.textContent = 'Sélectionnez au moins un besoin pour continuer.';
        error.hidden = false;
        needs[0].focus();
        return false;
      }
      return true;
    }

    quoteForm.addEventListener('submit', event => event.preventDefault());
    quoteForm.addEventListener('click', event => {
      if (event.target.closest('[data-next]') && validateStep()) showStep(Math.min(current + 1, panels.length));
      if (event.target.closest('[data-prev]')) showStep(Math.max(current - 1, 1));
      if (event.target.closest('[data-download-summary]')) {
        const lines = [
          'SIMULATION LOCALE NON OFFICIELLE — AUCUN DEVIS',
          '',
          ...summaryValues().map(([label, value]) => `${label} : ${value}`),
          '',
          'Ce document est un résumé indicatif sans tarif, sans valeur contractuelle et ne constitue pas une attestation.',
          'Aucune demande n’a été transmise à Allianz.'
        ];
        const blob = new Blob([lines.join('\n') + '\n'], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'recapitulatif-simulation-locale.txt';
        document.body.append(link);
        link.click();
        link.remove();
        window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      }
      if (event.target.closest('[data-print-summary]')) window.print();
    });
    quoteForm.addEventListener('change', () => clearError(current));
  }

  const tabsRoot = document.querySelector('[data-demo-tabs]');
  if (tabsRoot) {
    const tabs = [...tabsRoot.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
    function activate(index, focus = false) {
      tabs.forEach((tab, i) => {
        const selected = i === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        if (panels[i]) panels[i].hidden = !selected;
      });
      if (focus) tabs[index].focus();
    }
    tabs.forEach((tab, index) => {
      tab.disabled = false;
      tab.addEventListener('click', () => activate(index));
      tab.addEventListener('keydown', event => {
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(next, true);
      });
    });
    activate(0);
    const requestButton = tabsRoot.querySelector('[data-demo-request]');
    const requestStatus = tabsRoot.querySelector('[data-demo-request-status]');
    if (requestButton && requestStatus) {
      requestButton.disabled = false;
      requestButton.addEventListener('click', () => {
        requestStatus.textContent = 'Interaction de démonstration effectuée : aucune demande n’a été envoyée.';
      });
    }
  }
  document.querySelectorAll('[data-carousel]').forEach(track => {
    const section = track.closest('section');
    const previous = section && section.querySelector('[data-carousel-prev]');
    const next = section && section.querySelector('[data-carousel-next]');
    if (!previous || !next || !track.firstElementChild) return;
    function refreshButtons() {
      previous.disabled = track.scrollLeft <= 1;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
    }
    function move(direction) {
      const distance = track.firstElementChild.getBoundingClientRect().width + 18;
      track.scrollBy({ left: distance * direction, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    }
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('scroll', refreshButtons, { passive: true });
    window.addEventListener('resize', refreshButtons);
    refreshButtons();
  });
})();
