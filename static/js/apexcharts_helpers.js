/**
 * RetailMart V3 - ApexCharts Reusable Helper Library
 * Standardizes styling, dark navy themes, and Indian currency formatting.
 */

const RM_THEME = {
  navyDark: '#0F1F33',
  navyCard: '#183A5F',
  blueBorder: '#24598A',
  textWhite: '#FFFFFF',
  textLight: '#D5DCE5',
  textMuted: '#8E9BAE',
  purple: '#A459D0',
  pink: '#E95B9F',
  cyan: '#2CD4E1',
  orange: '#E88E3E',
  yellow: '#FFBD4A',
  grid: '#6F8298',
};

// Format currency in Indian standard: Crores, Lakhs, Thousands
function formatINR(val) {
  if (val === null || val === undefined || isNaN(val)) return '₹0';
  const num = Number(val);
  const abs = Math.abs(num);
  if (abs >= 10000000) {
    return '₹' + (num / 10000000).toFixed(2) + ' Cr';
  } else if (abs >= 100000) {
    return '₹' + (num / 100000).toFixed(2) + ' L';
  } else if (abs >= 1000) {
    return '₹' + (num / 1000).toFixed(1) + ' K';
  }
  return '₹' + num.toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

function getBaseChartOptions() {
  return {
    chart: {
      background: 'transparent',
      toolbar: { show: false },
      fontFamily: 'Inter, sans-serif',
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 400
      }
    },
    theme: { mode: 'dark' },
    grid: {
      borderColor: 'rgba(111, 130, 152, 0.25)',
      strokeDashArray: 3,
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } }
    },
    dataLabels: { enabled: false },
    tooltip: {
      theme: 'dark',
      style: { fontSize: '12px', fontFamily: 'Inter, sans-serif' },
      y: {
        formatter: function (val) {
          return typeof val === 'number' && val > 1000 ? formatINR(val) : val;
        }
      }
    }
  };
}

// 1. Line / Spline Area Chart
function renderAreaChart(containerId, categories, series, customOpts = {}) {
  const base = getBaseChartOptions();
  const options = {
    ...base,
    chart: { ...base.chart, type: 'area', height: customOpts.height || 280 },
    colors: customOpts.colors || [RM_THEME.purple, RM_THEME.cyan],
    stroke: { curve: 'smooth', width: 2.5 },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [0, 95, 100]
      }
    },
    series: series,
    xaxis: {
      categories: categories,
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' }
      },
      axisBorder: { color: RM_THEME.blueBorder },
      axisTicks: { color: RM_THEME.blueBorder }
    },
    yaxis: {
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' },
        formatter: customOpts.yFormatter || function (v) { return formatINR(v); }
      }
    },
    ...customOpts
  };

  const chart = new ApexCharts(document.querySelector('#' + containerId), options);
  chart.render();
  return chart;
}

// 2. Bar Chart (Vertical)
function renderBarChart(containerId, categories, series, customOpts = {}) {
  const base = getBaseChartOptions();
  const options = {
    ...base,
    chart: { ...base.chart, type: 'bar', height: customOpts.height || 280 },
    colors: customOpts.colors || [RM_THEME.cyan, RM_THEME.purple],
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        borderRadius: 4
      }
    },
    series: series,
    xaxis: {
      categories: categories,
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' },
        rotate: -20
      }
    },
    yaxis: {
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' },
        formatter: customOpts.yFormatter || function (v) { return typeof v === 'number' && v > 1000 ? formatINR(v) : v; }
      }
    },
    ...customOpts
  };

  const chart = new ApexCharts(document.querySelector('#' + containerId), options);
  chart.render();
  return chart;
}

// 3. Horizontal Bar Chart (Rankings, SLAs)
function renderHorizontalBarChart(containerId, categories, series, customOpts = {}) {
  const base = getBaseChartOptions();
  const options = {
    ...base,
    chart: { ...base.chart, type: 'bar', height: customOpts.height || 300 },
    colors: customOpts.colors || [RM_THEME.purple],
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 4,
        barHeight: '60%'
      }
    },
    series: series,
    xaxis: {
      categories: categories,
      labels: {
        style: { colors: RM_THEME.textMuted, fontSize: '11px' },
        formatter: customOpts.xFormatter || function (v) { return v; }
      }
    },
    yaxis: {
      labels: {
        style: { colors: RM_THEME.textLight, fontSize: '11px' }
      }
    },
    ...customOpts
  };

  const chart = new ApexCharts(document.querySelector('#' + containerId), options);
  chart.render();
  return chart;
}

// 4. Donut Chart (Payment modes, status distribution)
function renderDonutChart(containerId, labels, series, customOpts = {}) {
  const base = getBaseChartOptions();
  const options = {
    ...base,
    chart: { ...base.chart, type: 'donut', height: customOpts.height || 260 },
    colors: customOpts.colors || [RM_THEME.purple, RM_THEME.cyan, RM_THEME.pink, RM_THEME.orange, RM_THEME.yellow, '#4ADE80', '#60A5FA', '#F472B6'],
    labels: labels,
    series: series,
    plotOptions: {
      pie: {
        donut: {
          size: '68%',
          labels: {
            show: true,
            total: {
              show: true,
              label: customOpts.totalLabel || 'Total',
              color: RM_THEME.textLight,
              formatter: function (w) {
                const total = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                return typeof total === 'number' && total > 1000 ? formatINR(total) : total;
              }
            }
          }
        }
      }
    },
    legend: {
      position: 'bottom',
      labels: { colors: RM_THEME.textLight }
    },
    ...customOpts
  };

  const chart = new ApexCharts(document.querySelector('#' + containerId), options);
  chart.render();
  return chart;
}
