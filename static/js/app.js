/**
 * HealthRisk AI: Diabetes & Heart Disease Risk Predictor
 * Client-Side Controller (Vanilla JS - No NPM)
 * Powered by IBM watsonx.ai Architecture
 */

// Application State
const appState = {
    presets: null,
    metrics: null
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadPresets();
    loadMetrics();
});

/* ================= TAB NAVIGATION ================= */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

/* ================= PRESETS ================= */
async function loadPresets() {
    try {
        const res = await fetch('/api/presets');
        const json = await res.json();
        if (json.status === 'success') {
            appState.presets = json.data;
        }
    } catch (err) {
        console.warn('Could not load presets:', err);
    }
}

function loadDiabetesPreset(key) {
    if (!appState.presets || !appState.presets.diabetes || !appState.presets.diabetes[key]) return;
    const p = appState.presets.diabetes[key];
    document.getElementById('diab_glucose').value = p.glucose;
    document.getElementById('diab_bmi').value = p.bmi;
    document.getElementById('diab_bp').value = p.blood_pressure;
    document.getElementById('diab_age').value = p.age;
    document.getElementById('diab_insulin').value = p.insulin;
    document.getElementById('diab_dpf').value = p.dpf;
    document.getElementById('diab_pregnancies').value = p.pregnancies;
    document.getElementById('diab_skin').value = p.skin_thickness;

    document.getElementById('btnDiabPredict').click();
}

function loadHeartPreset(key) {
    if (!appState.presets || !appState.presets.heart || !appState.presets.heart[key]) return;
    const p = appState.presets.heart[key];
    document.getElementById('heart_age').value = p.age;
    document.getElementById('heart_sex').value = p.sex;
    document.getElementById('heart_cp').value = p.cp;
    document.getElementById('heart_trestbps').value = p.trestbps;
    document.getElementById('heart_chol').value = p.chol;
    document.getElementById('heart_fbs').value = p.fbs;
    document.getElementById('heart_restecg').value = p.restecg;
    document.getElementById('heart_thalach').value = p.thalach;
    document.getElementById('heart_exang').value = p.exang;
    document.getElementById('heart_oldpeak').value = p.oldpeak;
    document.getElementById('heart_slope').value = p.slope;
    document.getElementById('heart_ca').value = p.ca;
    document.getElementById('heart_thal').value = p.thal;

    document.getElementById('btnHeartPredict').click();
}

function resetDiabetesForm() {
    document.getElementById('diabetesForm').reset();
    document.getElementById('diabResultBody').innerHTML = `
        <div class="placeholder-state">
            <div class="placeholder-icon">📋</div>
            <h4>No Prediction Yet</h4>
            <p>Fill in the numbers on the left or click one of the <strong>Sample Profiles</strong> to check the risk.</p>
        </div>`;
    document.getElementById('diabBadge').className = 'badge';
    document.getElementById('diabBadge').textContent = 'Ready';
}

function resetHeartForm() {
    document.getElementById('heartForm').reset();
    document.getElementById('heartResultBody').innerHTML = `
        <div class="placeholder-state">
            <div class="placeholder-icon">🫀</div>
            <h4>No Prediction Yet</h4>
            <p>Fill in the numbers on the left or click one of the <strong>Sample Profiles</strong> to check the risk.</p>
        </div>`;
    document.getElementById('heartBadge').className = 'badge';
    document.getElementById('heartBadge').textContent = 'Ready';
}

/* ================= PREDICTION HANDLERS ================= */
async function handleDiabetesPredict(e) {
    e.preventDefault();
    const btn = document.getElementById('btnDiabPredict');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span>Checking Risk...</span>';
    btn.disabled = true;

    const payload = {
        glucose: document.getElementById('diab_glucose').value,
        bmi: document.getElementById('diab_bmi').value,
        blood_pressure: document.getElementById('diab_bp').value,
        age: document.getElementById('diab_age').value,
        insulin: document.getElementById('diab_insulin').value,
        dpf: document.getElementById('diab_dpf').value,
        pregnancies: document.getElementById('diab_pregnancies').value,
        skin_thickness: document.getElementById('diab_skin').value
    };

    try {
        const res = await fetch('/api/predict/diabetes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        if (result.status === 'success') {
            renderPredictionResult('diab', result, 'Diabetes');
        } else {
            alert('Prediction error: ' + result.message);
        }
    } catch (err) {
        alert('Server connection error: ' + err.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

async function handleHeartPredict(e) {
    e.preventDefault();
    const btn = document.getElementById('btnHeartPredict');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span>Checking Risk...</span>';
    btn.disabled = true;

    const payload = {
        age: document.getElementById('heart_age').value,
        sex: document.getElementById('heart_sex').value,
        cp: document.getElementById('heart_cp').value,
        trestbps: document.getElementById('heart_trestbps').value,
        chol: document.getElementById('heart_chol').value,
        fbs: document.getElementById('heart_fbs').value,
        restecg: document.getElementById('heart_restecg').value,
        thalach: document.getElementById('heart_thalach').value,
        exang: document.getElementById('heart_exang').value,
        oldpeak: document.getElementById('heart_oldpeak').value,
        slope: document.getElementById('heart_slope').value,
        ca: document.getElementById('heart_ca').value,
        thal: document.getElementById('heart_thal').value
    };

    try {
        const res = await fetch('/api/predict/heart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        if (result.status === 'success') {
            renderPredictionResult('heart', result, 'Heart Disease');
        } else {
            alert('Prediction error: ' + result.message);
        }
    } catch (err) {
        alert('Server connection error: ' + err.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

/* ================= RENDER RESULT ================= */
function renderPredictionResult(prefix, data, diseaseName) {
    const badge = document.getElementById(`${prefix}Badge`);
    const body = document.getElementById(`${prefix}ResultBody`);

    badge.className = `badge badge-${data.risk_color}`;
    badge.textContent = data.risk_level;

    // SVG Dial Calculation (radius = 48)
    const radius = 48;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (data.risk_score / 100) * circumference;

    let strokeColor = '#10b981'; // Green
    if (data.risk_color === 'warning') strokeColor = '#f59e0b'; // Amber
    if (data.risk_color === 'danger') strokeColor = '#ef4444'; // Red

    const factorsHtml = data.risk_factors.map(f => `
        <div class="factor-tag ${f.includes('High') || f.includes('Borderline') || f.includes('Elevated') || f.includes('discomfort') || f.includes('Blocked') ? 'flagged' : ''}">
            ${f}
        </div>
    `).join('');

    const tipsHtml = data.recommendations.map(r => `<li>${r}</li>`).join('');

    body.innerHTML = `
        <div class="result-hero">
            <div class="dial-wrap">
                <svg width="120" height="120">
                    <circle class="dial-bg" cx="60" cy="60" r="${radius}"></circle>
                    <circle class="dial-bar" cx="60" cy="60" r="${radius}" 
                            stroke="${strokeColor}"
                            stroke-dasharray="${circumference}" 
                            stroke-dashoffset="${offset}"></circle>
                </svg>
                <div class="dial-txt">
                    <span class="dial-score" style="color: ${strokeColor};">${data.risk_score}%</span>
                    <span class="dial-lbl">Risk Score</span>
                </div>
            </div>

            <div class="result-meta">
                <div class="status-badge badge-${data.risk_color}">
                    ${data.risk_level}
                </div>
                <span class="model-source">${data.engine_used}</span>
            </div>
        </div>

        <div class="summary-card">
            ${data.summary}
        </div>

        <div class="section-group">
            <h4>Key Health Factors</h4>
            <div class="factor-tags">
                ${factorsHtml}
            </div>
        </div>

        <div class="section-group">
            <h4>Healthy Suggestions</h4>
            <ul class="tips-list">
                ${tipsHtml}
            </ul>
        </div>

        <div class="result-footer">
            <button class="btn btn-sub btn-sm" onclick="window.print()">
                🖨️ Print / Save Summary (PDF)
            </button>
        </div>
    `;
}

/* ================= STATS TAB ================= */
async function loadMetrics(forceReload = false) {
    if (appState.metrics && !forceReload) {
        renderMetrics(appState.metrics);
        return;
    }

    try {
        const res = await fetch('/api/metrics');
        const json = await res.json();
        if (json.status === 'success') {
            appState.metrics = json.data;
            renderMetrics(json.data);
        }
    } catch (err) {
        console.warn('Could not load metrics:', err);
    }
}

function renderMetrics(data) {
    if (data.diabetes) {
        const d = data.diabetes;
        document.getElementById('diabModelName').textContent = 'Random Forest';
        document.getElementById('diabAcc').textContent = d.accuracy + '%';
        document.getElementById('diabAuc').textContent = d.auc_roc + '%';
        document.getElementById('diabPrec').textContent = d.precision + '%';
        document.getElementById('diabF1').textContent = d.f1_score + '%';

        renderConfusionMatrix('diabCmTable', d.confusion_matrix, 'Healthy', 'Diabetic');
        renderFeatureImportance('diabFeatList', d.feature_importance);
    }

    if (data.heart) {
        const h = data.heart;
        document.getElementById('heartModelName').textContent = 'Random Forest';
        document.getElementById('heartAcc').textContent = h.accuracy + '%';
        document.getElementById('heartAuc').textContent = h.auc_roc + '%';
        document.getElementById('heartPrec').textContent = h.precision + '%';
        document.getElementById('heartF1').textContent = h.f1_score + '%';

        renderConfusionMatrix('heartCmTable', h.confusion_matrix, 'Healthy', 'Heart Risk');
        renderFeatureImportance('heartFeatList', h.feature_importance);
    }
}

function renderConfusionMatrix(containerId, cm, label0, label1) {
    const el = document.getElementById(containerId);
    if (!el || !cm) return;

    el.innerHTML = `
        <table class="cm-table">
            <thead>
                <tr>
                    <th>Actual \\ Predicted</th>
                    <th>Predicted ${label0}</th>
                    <th>Predicted ${label1}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Actual ${label0}</strong></td>
                    <td class="cm-correct">Correct: ${cm.tn}</td>
                    <td class="cm-wrong">Missed: ${cm.fp}</td>
                </tr>
                <tr>
                    <td><strong>Actual ${label1}</strong></td>
                    <td class="cm-wrong">Missed: ${cm.fn}</td>
                    <td class="cm-correct">Correct: ${cm.tp}</td>
                </tr>
            </tbody>
        </table>
    `;
}

function renderFeatureImportance(containerId, list) {
    const el = document.getElementById(containerId);
    if (!el || !list) return;

    const topItems = list.slice(0, 5);
    el.innerHTML = topItems.map(item => `
        <div class="feat-row">
            <div class="feat-meta">
                <span><strong>${item.feature}</strong></span>
                <span>${item.importance}%</span>
            </div>
            <div class="feat-bg">
                <div class="feat-fill" style="width: ${item.importance}%;"></div>
            </div>
        </div>
    `).join('');
}
