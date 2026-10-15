/**
 * RetailMart V3 - Filter Interaction Controller
 * Handles cascading store dropdowns, auto-filtering on selection, date presets, and filter resets.
 */

document.addEventListener('DOMContentLoaded', () => {
  const regionSelect = document.getElementById('filter-region');
  const storeSelect = document.getElementById('filter-store');
  const catSelect = document.getElementById('filter-category');
  const tierSelect = document.getElementById('filter-tier');
  const resetBtn = document.getElementById('btn-reset-filters');
  const filterForm = document.getElementById('global-filter-form');
  const applyBtns = document.querySelectorAll('button[type="submit"]');

  function submitWithFeedback() {
    applyBtns.forEach(btn => {
      btn.innerHTML = '<i class="ti ti-loader-2" style="animation: spin 1s linear infinite;"></i> Filtering...';
      btn.disabled = true;
      btn.style.opacity = '0.8';
    });
    filterForm.submit();
  }

  // 1. Changing Region resets Store and auto-submits so server cascades stores & filters data
  if (regionSelect && filterForm) {
    regionSelect.addEventListener('change', () => {
      if (storeSelect) {
        storeSelect.value = ''; // Reset to all stores within the newly chosen region
      }
      submitWithFeedback();
    });
  }

  // 2. Changing Store auto-submits
  if (storeSelect && filterForm) {
    storeSelect.addEventListener('change', () => {
      submitWithFeedback();
    });
  }

  // 3. Changing Product Category auto-submits
  if (catSelect && filterForm) {
    catSelect.addEventListener('change', () => {
      submitWithFeedback();
    });
  }

  // 4. Changing Customer Tier auto-submits
  if (tierSelect && filterForm) {
    tierSelect.addEventListener('change', () => {
      submitWithFeedback();
    });
  }

  // 5. Form submission via Apply button
  if (filterForm) {
    filterForm.addEventListener('submit', () => {
      applyBtns.forEach(btn => {
        btn.innerHTML = '<i class="ti ti-loader-2" style="animation: spin 1s linear infinite;"></i> Filtering...';
      });
    });
  }

  // 6. Filter Reset Button
  if (resetBtn && filterForm) {
    resetBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const startDateInput = document.getElementById('filter-start-date');
      const endDateInput = document.getElementById('filter-end-date');
      if (startDateInput) startDateInput.value = '2024-01-01';
      if (endDateInput) endDateInput.value = '2026-02-26';
      if (regionSelect) regionSelect.value = '';
      if (storeSelect) storeSelect.value = '';
      if (catSelect) catSelect.value = '';
      if (tierSelect) tierSelect.value = '';
      
      submitWithFeedback();
    });
  }
});

// Helper for date presets
function applyDatePreset(preset) {
  const startInput = document.getElementById('filter-start-date');
  const endInput = document.getElementById('filter-end-date');
  const form = document.getElementById('global-filter-form');
  if (!startInput || !endInput || !form) return;
  
  const now = new Date('2026-02-26');
  let startDate = new Date('2024-01-01');
  let endDate = new Date('2026-02-26');
  
  if (preset === '30d') {
    startDate = new Date(now);
    startDate.setDate(now.getDate() - 30);
  } else if (preset === '90d') {
    startDate = new Date(now);
    startDate.setDate(now.getDate() - 90);
  } else if (preset === '2025') {
    startDate = new Date('2025-01-01');
    endDate = new Date('2025-12-31');
  } else if (preset === 'all') {
    startDate = new Date('2024-01-01');
    endDate = new Date('2026-02-26');
  }
  
  startInput.value = startDate.toISOString().split('T')[0];
  endInput.value = endDate.toISOString().split('T')[0];
  
  const applyBtns = document.querySelectorAll('button[type="submit"]');
  applyBtns.forEach(btn => {
    btn.innerHTML = '<i class="ti ti-loader-2" style="animation: spin 1s linear infinite;"></i> Filtering...';
  });
  
  form.submit();
}
