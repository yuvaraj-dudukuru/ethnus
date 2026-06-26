/* ============================================================================
 *  dashboard.js — ALL of the Module 6 front-end logic for the ANALYTICS page.
 * ----------------------------------------------------------------------------
 *  The page never reloads. It makes ONE call to /api/stats/, then spreads that
 *  single response across four stat cards and three charts.
 *
 *  ⭐ THE STAR SKILL: turning API JSON into chart data.
 *     The server sends arrays like:
 *         "by_department": [ {"label": "Physics", "count": 12}, ... ]
 *     Chart.js wants TWO parallel arrays instead:
 *         labels: ["Physics", ...]      data: [12, ...]
 *     So for every chart we MAP the results into labels[] and data[]. That
 *     "reshape the JSON" step is the whole job of a charting front-end.
 *
 *  Also shown here:
 *     - SKELETON loaders while the data is being fetched,
 *     - a DATE-RANGE filter that re-fetches everything with ?start=&end=.
 *
 *  Open DevTools → Network tab to watch the single /api/stats/ request.
 * ==========================================================================*/

document.addEventListener('DOMContentLoaded', function () {

    const API = '/api';

    // Grab the elements once.
    const el = {
        filterForm: document.getElementById('filter-form'),
        fStart:     document.getElementById('f-start'),
        fEnd:       document.getElementById('f-end'),
        fReset:     document.getElementById('f-reset'),
        rangeLabel: document.getElementById('range-label'),
        flash:      document.getElementById('flash'),
        passmark:   document.getElementById('passmark'),
        // cards
        cardTotal:   document.getElementById('card-total'),
        cardAverage: document.getElementById('card-average'),
        cardTop:     document.getElementById('card-top'),
        cardActive:  document.getElementById('card-active'),
    };

    // We keep the Chart.js instances so we can destroy & redraw them on refresh.
    const charts = { bar: null, line: null, doughnut: null };

    const show = n => n.classList.remove('d-none');
    const hide = n => n.classList.add('d-none');

    function showError(message) {
        el.flash.textContent = message;
        show(el.flash);
    }

    // ------------------------------------------------------------------
    //  SKELETONS — show grey placeholders while loading, hide them after.
    // ------------------------------------------------------------------
    function showSkeletons() {
        // Charts: show the grey block, hide the real canvas box.
        ['bar', 'line', 'doughnut'].forEach(key => {
            show(document.getElementById('sk-' + key));
            hide(document.getElementById('box-' + key));
        });
        // Cards: drop a small shimmer bar into each value.
        const bar = '<span class="skeleton skeleton-line d-inline-block" style="width:60px">&nbsp;</span>';
        el.cardTotal.innerHTML = bar;
        el.cardAverage.innerHTML = bar;
        el.cardActive.innerHTML = bar;
        el.cardTop.innerHTML = '<span class="skeleton skeleton-line d-inline-block" style="width:100px">&nbsp;</span>';
    }
    function hideChartSkeleton(key) {
        hide(document.getElementById('sk-' + key));
        show(document.getElementById('box-' + key));
    }

    // ------------------------------------------------------------------
    //  LOAD STATS (one request feeds the whole page)
    // ------------------------------------------------------------------
    async function loadStats() {
        hide(el.flash);
        showSkeletons();

        // Build the URL from the date filter (only add a date if it is set).
        const params = new URLSearchParams();
        if (el.fStart.value) params.set('start', el.fStart.value);
        if (el.fEnd.value)   params.set('end', el.fEnd.value);
        const url = API + '/stats/' + (params.toString() ? '?' + params.toString() : '');

        try {
            const res = await fetch(url);
            if (!res.ok) { showError('Could not load analytics (status ' + res.status + ').'); return; }
            const stats = await res.json();
            renderCards(stats.cards);
            renderBar(stats.by_department);
            renderDoughnut(stats.pass_fail);
            renderLine(stats.admissions_by_month);
            el.passmark.textContent = stats.pass_fail.pass_mark;
            updateRangeLabel();
        } catch (err) {
            showError('Could not reach the server for analytics.');
            console.error(err);
        }
    }

    // ------------------------------------------------------------------
    //  STAT CARDS
    // ------------------------------------------------------------------
    function renderCards(cards) {
        el.cardTotal.textContent   = cards.total;
        el.cardAverage.textContent = cards.average;
        el.cardActive.textContent  = cards.active;
        el.cardTop.textContent = cards.top_scorer
            ? `${cards.top_scorer.name} (${cards.top_scorer.marks})`
            : '—';
    }

    // ------------------------------------------------------------------
    //  CHARTS  — each one MAPS the JSON array into labels[] and data[]
    // ------------------------------------------------------------------

    // BAR: students per department.
    function renderBar(byDept) {
        // ⭐ map the [{label, count}] array into the two arrays Chart.js needs.
        const labels = byDept.map(row => row.label);
        const data   = byDept.map(row => row.count);

        if (charts.bar) charts.bar.destroy();         // clear the old chart first
        hideChartSkeleton('bar');
        charts.bar = new Chart(document.getElementById('chart-bar'), {
            type: 'bar',
            data: {
                labels,
                datasets: [{ label: 'Students', data, backgroundColor: '#0d6efd' }],
            },
            options: { responsive: true, maintainAspectRatio: false,
                       plugins: { legend: { display: false } },
                       scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
        });
    }

    // LINE: admissions per month.
    function renderLine(byMonth) {
        const labels = byMonth.map(row => row.label);
        const data   = byMonth.map(row => row.count);

        if (charts.line) charts.line.destroy();
        hideChartSkeleton('line');
        charts.line = new Chart(document.getElementById('chart-line'), {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Admissions', data,
                    borderColor: '#198754', backgroundColor: 'rgba(25,135,84,.15)',
                    fill: true, tension: 0.3,
                }],
            },
            options: { responsive: true, maintainAspectRatio: false,
                       scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
        });
    }

    // DOUGHNUT: pass vs fail (a small object, not an array).
    function renderDoughnut(passFail) {
        const labels = ['Pass', 'Fail'];
        const data   = [passFail.pass, passFail.fail];

        if (charts.doughnut) charts.doughnut.destroy();
        hideChartSkeleton('doughnut');
        charts.doughnut = new Chart(document.getElementById('chart-doughnut'), {
            type: 'doughnut',
            data: {
                labels,
                datasets: [{ data, backgroundColor: ['#198754', '#dc3545'] }],
            },
            options: { responsive: true, maintainAspectRatio: false },
        });
    }

    // ------------------------------------------------------------------
    //  DATE-RANGE FILTER
    // ------------------------------------------------------------------
    function updateRangeLabel() {
        const s = el.fStart.value, e = el.fEnd.value;
        if (s && e)      el.rangeLabel.textContent = `${s} → ${e}`;
        else if (s)      el.rangeLabel.textContent = `from ${s}`;
        else if (e)      el.rangeLabel.textContent = `up to ${e}`;
        else             el.rangeLabel.textContent = 'all dates';
    }

    el.filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        loadStats();          // re-fetch EVERYTHING with the new date range
    });

    el.fReset.addEventListener('click', function () {
        el.fStart.value = '';
        el.fEnd.value = '';
        loadStats();
    });

    // ------------------------------------------------------------------
    //  START
    // ------------------------------------------------------------------
    loadStats();   // first load: skeletons → one /api/stats/ call → cards + charts
});
