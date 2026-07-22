// =========================================================
// PHISHGUARD AI — FRONTEND LOGIC
// =========================================================

(function () {
  'use strict';

  const form = document.getElementById('scanner-form');
  const urlInput = document.getElementById('url-input');
  const analyzeBtn = document.getElementById('analyze-btn');

  const resultCard = document.getElementById('result-card');
  const resultIcon = document.getElementById('result-icon');
  const resultLabel = document.getElementById('result-label');
  const resultUrl = document.getElementById('result-url');

  const confidenceValue = document.getElementById('confidence-value');
  const confidenceFill = document.getElementById('confidence-fill');
  const confidenceBar = document.getElementById('confidence-bar');

  const metricAccuracy = document.getElementById('metric-accuracy');
  const metricPrecision = document.getElementById('metric-precision');
  const metricRecall = document.getElementById('metric-recall');
  const metricF1 = document.getElementById('metric-f1');

  const featureList = document.getElementById('feature-list');

  const navToggle = document.getElementById('nav-toggle');
  const primaryNav = document.getElementById('primary-nav');

  const ICONS = {
    legitimate: '✅',
    phishing: '⚠️'
  };

  // ---------- Mobile nav toggle ----------
  if (navToggle && primaryNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = primaryNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    primaryNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        primaryNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ---------- Form submission ----------
  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const url = urlInput.value.trim();
    if (!url) {
      urlInput.focus();
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
    url,
    model: document.getElementById("model").value
})
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      renderResult(data, url);
    } catch (error) {
      renderError(error);
    } finally {
      setLoading(false);
    }
  });

  // ---------- Loading state ----------
  function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    analyzeBtn.classList.toggle('is-loading', isLoading);
  }

  // ---------- Render success ----------
  function renderResult(data, submittedUrl) {
    const prediction = String(data.prediction || '').toLowerCase();
    const isLegitimate = prediction === 'legitimate';
    const verdict = isLegitimate ? 'legitimate' : 'phishing';

    resultCard.setAttribute('data-verdict', verdict);
    resultCard.hidden = false;

    resultIcon.textContent = isLegitimate ? ICONS.legitimate : ICONS.phishing;
    resultLabel.textContent = isLegitimate ? 'Legitimate Website' : 'Phishing Website';
    resultUrl.textContent = submittedUrl;

    const confidence = clampPercentage(data.confidence);
    confidenceValue.textContent = `${confidence.toFixed(1)}%`;
    confidenceFill.style.width = `${confidence}%`;
    confidenceBar.setAttribute('aria-valuenow', String(confidence));

    updateMetrics(data);
    updateFeatures(data.features || {});

    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // ---------- Render error ----------
  function renderError(error) {
    resultCard.setAttribute('data-verdict', 'phishing');
    resultCard.hidden = false;

    resultIcon.textContent = '⚠️';
    resultLabel.textContent = 'Analysis Failed';
    resultUrl.textContent = 'Could not reach the prediction service. Please try again.';

    confidenceValue.textContent = '0%';
    confidenceFill.style.width = '0%';
    confidenceBar.setAttribute('aria-valuenow', '0');

    featureList.querySelectorAll('[data-status]').forEach((el) => {
      el.textContent = '—';
      el.removeAttribute('data-value');
    });

    console.error('PhishGuard AI prediction error:', error);
  }

  // ---------- Update performance metrics ----------
  function updateMetrics(data) {
    if (typeof data.accuracy === 'number') {
      metricAccuracy.textContent = `${data.accuracy.toFixed(1)}%`;
    }
    if (typeof data.precision === 'number') {
      metricPrecision.textContent = `${data.precision.toFixed(1)}%`;
    }
    if (typeof data.recall === 'number') {
      metricRecall.textContent = `${data.recall.toFixed(1)}%`;
    }
    if (typeof data.f1 === 'number') {
      metricF1.textContent = `${data.f1.toFixed(1)}%`;
    }
  }

  // ---------- Update feature audit list ----------
  function updateFeatures(features) {

    const featureMap = {
        "https": features.SSLfinal_State,
        "ip": features.having_IP_Address,
        "at": features.having_At_Symbol,
        "subdomain": features.having_Sub_Domain,
        "length": features.URL_Length,
        "shortener": features.Shortining_Service
    };

    document.querySelectorAll(".feature-item").forEach(item => {

        const featureName = item.dataset.feature;
        const value = featureMap[featureName];

        item.classList.remove("safe", "danger", "warning");

        const icon = item.querySelector(".feature-icon");

        if (!icon) return;

        if (value === 1) {

            icon.innerHTML = "✓";
            item.classList.add("safe");

        }
        else if (value === -1) {

            icon.innerHTML = "✗";
            item.classList.add("danger");

        }
        else {

            icon.innerHTML = "!";
            item.classList.add("warning");

        }

    });

}

  // ---------- Helpers ----------
  function clampPercentage(value) {
    const num = Number(value);
    if (Number.isNaN(num)) return 0;
    return Math.min(100, Math.max(0, num));
  }
})();