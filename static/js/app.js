// static/js/app.js - Frontend interactivity

const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
if (hamburger) {
    hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
}

// Radio card selection highlighting
document.querySelectorAll('.radio-card').forEach(card => {
    const input = card.querySelector('input[type="radio"]');
    if (input && input.checked) card.classList.add('selected');
    card.addEventListener('click', () => {
        const name = input ? input.name : null;
        if (name) {
            document.querySelectorAll(`input[name="${name}"]`).forEach(inp => {
                inp.closest('.radio-card')?.classList.remove('selected');
            });
        }
        card.classList.add('selected');
    });
});

// Live BMI calculator on profile page
const weightInput = document.querySelector('input[name="weight_kg"]');
const heightInput = document.querySelector('input[name="height_cm"]');

function updateBMI() {
    const weight = parseFloat(weightInput?.value);
    const height = parseFloat(heightInput?.value);
    if (!weight || !height || height <= 0) return;
    const bmi = (weight / Math.pow(height / 100, 2)).toFixed(1);
    let category = bmi < 18.5 ? 'Underweight' : bmi < 25 ? 'Normal' : bmi < 30 ? 'Overweight' : 'Obese';
    let cssClass = 'bmi-' + category.toLowerCase();
    let bmiDisplay = document.getElementById('live-bmi');
    if (!bmiDisplay) {
        bmiDisplay = document.createElement('div');
        bmiDisplay.id = 'live-bmi';
        bmiDisplay.className = 'bmi-display';
        const grid = document.querySelector('.form-grid');
        if (grid) grid.after(bmiDisplay);
    }
    bmiDisplay.innerHTML = `<span class="bmi-value">BMI: <strong>${bmi}</strong></span>
        <span class="bmi-badge ${cssClass}">${category}</span>
        <small style="color:var(--text-muted);font-size:0.78rem">Auto-calculated</small>`;
}

if (weightInput) weightInput.addEventListener('input', updateBMI);
if (heightInput) heightInput.addEventListener('input', updateBMI);

// Button loading state
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        const btn = form.querySelector('button[type="submit"]');
        if (btn) { btn.disabled = true; btn.textContent = 'Processing...'; }
    });
});

// Smooth scroll to hash
if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 300);
}
