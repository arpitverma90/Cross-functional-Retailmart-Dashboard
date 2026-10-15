/**
 * RetailMart V3 - Contribution Margin Scenario Simulator
 * Interactive client-side what-if calculator with baseline comparison.
 */

let simChart = null;

function initSimulator(baseline) {
  const sliderVolume = document.getElementById('sim-volume');
  const sliderPrice = document.getElementById('sim-price');
  const sliderReturn = document.getElementById('sim-return');
  const sliderCost = document.getElementById('sim-cost');
  
  const valVolume = document.getElementById('val-volume');
  const valPrice = document.getElementById('val-price');
  const valReturn = document.getElementById('val-return');
  const valCost = document.getElementById('val-cost');
  
  const simRevEl = document.getElementById('sim-rev');
  const simMarginEl = document.getElementById('sim-margin');
  const simMarginPctEl = document.getElementById('sim-margin-pct');
  const simVarEl = document.getElementById('sim-var');
  
  function recalculate() {
    const volPct = parseFloat(sliderVolume.value) / 100;
    const pricePct = parseFloat(sliderPrice.value) / 100;
    const returnPct = parseFloat(sliderReturn.value) / 100;
    const costPct = parseFloat(sliderCost.value) / 100;
    
    valVolume.textContent = (volPct >= 0 ? '+' : '') + (volPct * 100).toFixed(0) + '%';
    valPrice.textContent = (pricePct >= 0 ? '+' : '') + (pricePct * 100).toFixed(1) + '%';
    valReturn.textContent = (returnPct >= 0 ? '+' : '') + (returnPct * 100).toFixed(0) + '%';
    valCost.textContent = (costPct >= 0 ? '+' : '') + (costPct * 100).toFixed(0) + '%';
    
    // Formula:
    // Simulated Net Revenue = Base Revenue * (1 + volPct) * (1 + pricePct)
    // Simulated COGS = Base COGS * (1 + volPct)
    // Simulated Refunds = Base Refunds * (1 + returnPct) * (1 + volPct)
    // Simulated Operating Expenses = Base Expenses * (1 + costPct)
    
    const simRevenue = baseline.base_net_revenue * (1 + volPct) * (1 + pricePct);
    const simCogs = baseline.base_cogs * (1 + volPct);
    const simRefunds = baseline.base_refunds * (1 + returnPct) * (1 + volPct);
    const simExpenses = baseline.base_store_expenses * (1 + costPct);
    
    const simContributionMargin = simRevenue - simCogs - simRefunds - simExpenses;
    const simMarginPct = (simContributionMargin / simRevenue) * 100;
    const variance = simContributionMargin - baseline.base_contribution_margin;
    const varPct = (variance / baseline.base_contribution_margin) * 100;
    
    simRevEl.textContent = formatINR(simRevenue);
    simMarginEl.textContent = formatINR(simContributionMargin);
    simMarginPctEl.textContent = simMarginPct.toFixed(2) + '%';
    
    simVarEl.textContent = (variance >= 0 ? '+' : '') + formatINR(variance) + ' (' + (varPct >= 0 ? '+' : '') + varPct.toFixed(1) + '%)';
    simVarEl.className = 'kpi-badge ' + (variance >= 0 ? 'badge-positive' : 'badge-negative');
    
    // Update chart
    if (simChart) {
      simChart.updateSeries([
        {
          name: 'Baseline Actuals',
          data: [
            Math.round(baseline.base_net_revenue / 10000000),
            Math.round(baseline.base_cogs / 10000000),
            Math.round(baseline.base_refunds / 10000000),
            Math.round(baseline.base_store_expenses / 10000000),
            Math.round(baseline.base_contribution_margin / 10000000)
          ]
        },
        {
          name: 'Simulated Scenario',
          data: [
            Math.round(simRevenue / 10000000),
            Math.round(simCogs / 10000000),
            Math.round(simRefunds / 10000000),
            Math.round(simExpenses / 10000000),
            Math.round(simContributionMargin / 10000000)
          ]
        }
      ]);
    }
  }
  
  [sliderVolume, sliderPrice, sliderReturn, sliderCost].forEach(slider => {
    slider.addEventListener('input', recalculate);
  });
  
  document.getElementById('btn-reset-sim').addEventListener('click', () => {
    sliderVolume.value = 0;
    sliderPrice.value = 0;
    sliderReturn.value = 0;
    sliderCost.value = 0;
    recalculate();
  });
  
  // Render Comparison Chart
  const chartOptions = {
    ...getBaseChartOptions(),
    chart: { type: 'bar', height: 320, toolbar: { show: false } },
    colors: [RM_THEME.grid, RM_THEME.purple],
    plotOptions: {
      bar: { horizontal: false, columnWidth: '45%', borderRadius: 4 }
    },
    series: [
      {
        name: 'Baseline Actuals (₹ Cr)',
        data: [
          Math.round(baseline.base_net_revenue / 10000000),
          Math.round(baseline.base_cogs / 10000000),
          Math.round(baseline.base_refunds / 10000000),
          Math.round(baseline.base_store_expenses / 10000000),
          Math.round(baseline.base_contribution_margin / 10000000)
        ]
      },
      {
        name: 'Simulated Scenario (₹ Cr)',
        data: [
          Math.round(baseline.base_net_revenue / 10000000),
          Math.round(baseline.base_cogs / 10000000),
          Math.round(baseline.base_refunds / 10000000),
          Math.round(baseline.base_store_expenses / 10000000),
          Math.round(baseline.base_contribution_margin / 10000000)
        ]
      }
    ],
    xaxis: {
      categories: ['Net Revenue', 'COGS', 'Refunds', 'Store Expenses', 'Contribution Margin'],
      labels: { style: { colors: RM_THEME.textLight, fontSize: '11px' } }
    },
    yaxis: {
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' },
        formatter: function(val) { return '₹' + val + ' Cr'; }
      }
    },
    legend: { position: 'top', labels: { colors: RM_THEME.textLight } }
  };
  
  simChart = new ApexCharts(document.getElementById('sim-comparison-chart'), chartOptions);
  simChart.render();
  
  recalculate();
}
