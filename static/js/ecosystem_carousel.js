/**
 * ecosystem_carousel.js - GG Solutions Ecosystem Carousel & Lightweight UI Micro-Simulations
 * Handles horizontal carousel navigation, exact 3-cards-per-view calculation on desktop,
 * drag-to-scroll, and realistic micro-interactions for the 6 core systems:
 * (Opportunity, Club DRS, Telemetrías, EduAgro, Pilates, Mercotruck).
 */

document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('ecosystem-carousel-wrapper');
    const track = document.getElementById('ecosystem-carousel-track');
    const prevBtn = document.getElementById('carousel-prev-btn');
    const nextBtn = document.getElementById('carousel-next-btn');
    const currentIndexEl = document.getElementById('carousel-current-index');
    const cards = document.querySelectorAll('.carousel-card');
    const pageDots = document.querySelectorAll('.page-dot');

    if (!wrapper || !track || cards.length === 0) return;

    let currentIndex = 0;
    const totalCards = cards.length;

    // Helper: Pad number with leading zero
    const formatIndex = (idx) => String(idx + 1).padStart(2, '0');

    // 0. Auto-calculate exact card width so 3 cards fit on desktop without cutting off
    function updateResponsiveCardWidth() {
        const w = wrapper.clientWidth;
        if (window.innerWidth >= 1024) {
            // Exactly 3 cards visible with 2 gaps of 24px = 48px
            const cardW = Math.floor((w - 48) / 3);
            wrapper.style.setProperty('--card-w', `${cardW}px`);
        } else if (window.innerWidth >= 768) {
            // Exactly 2 cards visible with 1 gap of 20px
            const cardW = Math.floor((w - 20) / 2);
            wrapper.style.setProperty('--card-w', `${cardW}px`);
        } else {
            // Mobile: keep 84vw
            wrapper.style.removeProperty('--card-w');
        }
    }
    updateResponsiveCardWidth();
    window.addEventListener('resize', updateResponsiveCardWidth);

    // 1. Navigation by index
    function scrollToIndex(idx) {
        if (idx < 0) idx = 0;
        if (idx >= totalCards) idx = totalCards - 1;

        currentIndex = idx;
        const targetCard = cards[idx];
        if (!targetCard) return;

        const cardLeft = targetCard.offsetLeft - track.offsetLeft;
        wrapper.scrollTo({
            left: cardLeft,
            behavior: 'smooth'
        });

        updateUIState(idx);
    }

    function updateUIState(idx) {
        if (currentIndexEl) {
            currentIndexEl.textContent = formatIndex(idx);
        }

        pageDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === idx);
        });

        if (prevBtn) {
            prevBtn.style.opacity = idx === 0 ? '0.45' : '1';
        }
        if (nextBtn) {
            nextBtn.style.opacity = idx === totalCards - 1 ? '0.45' : '1';
        }
    }

    // Button click listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            scrollToIndex(currentIndex - 1);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            scrollToIndex(currentIndex + 1);
        });
    }

    // Dot indicators click
    pageDots.forEach((dot) => {
        dot.addEventListener('click', (e) => {
            const idx = parseInt(e.currentTarget.getAttribute('data-index'), 10);
            if (!isNaN(idx)) {
                scrollToIndex(idx);
            }
        });
    });

    // 2. Scroll detection with IntersectionObserver on cards
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
                const idx = parseInt(entry.target.getAttribute('data-index'), 10);
                if (!isNaN(idx)) {
                    currentIndex = idx;
                    updateUIState(idx);
                }
            }
        });
    }, {
        root: wrapper,
        threshold: 0.5
    });

    cards.forEach(card => cardObserver.observe(card));

    // 3. Desktop Drag-to-Scroll support
    let isDown = false;
    let startX = 0;
    let scrollLeftStart = 0;

    wrapper.addEventListener('mousedown', (e) => {
        if (e.target.closest('a, button')) return;
        isDown = true;
        wrapper.style.cursor = 'grabbing';
        wrapper.style.scrollBehavior = 'auto';
        startX = e.pageX - wrapper.offsetLeft;
        scrollLeftStart = wrapper.scrollLeft;
    });

    wrapper.addEventListener('mouseleave', () => {
        if (!isDown) return;
        isDown = false;
        wrapper.style.cursor = '';
        wrapper.style.scrollBehavior = 'smooth';
    });

    wrapper.addEventListener('mouseup', () => {
        if (!isDown) return;
        isDown = false;
        wrapper.style.cursor = '';
        wrapper.style.scrollBehavior = 'smooth';
    });

    wrapper.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - wrapper.offsetLeft;
        const walk = (x - startX) * 1.5;
        wrapper.scrollLeft = scrollLeftStart - walk;
    });

    // 4. Keyboard Arrow Navigation
    wrapper.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            scrollToIndex(currentIndex + 1);
        } else if (e.key === 'ArrowLeft') {
            scrollToIndex(currentIndex - 1);
        }
    });

    // Initialize UI
    updateUIState(0);

    // =========================================================================
    // 5. REALISTIC MICRO-SIMULATIONS LOOP (Optimized with IntersectionObserver)
    // =========================================================================
    let simulationActive = false;
    let simInterval = null;

    const casesSection = document.getElementById('cases');
    if (!casesSection) return;

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (!simulationActive) {
                    startMicroSimulations();
                }
            } else {
                stopMicroSimulations();
            }
        });
    }, { threshold: 0.15 });

    sectionObserver.observe(casesSection);

    function startMicroSimulations() {
        simulationActive = true;

        // Elements for Opportunity (Stages Tabs)
        const oppTabs = document.querySelectorAll('.opp-stage-tab');
        let currentOppTab = 0;

        // Elements for Club DRS (Countdown widget seconds ticker)
        const cdSec = document.querySelector('.cd-sec');
        let secCounter = 14;

        // Elements for Telemetría (Lap time delta & leader gap)
        const telGap = document.querySelector('.lap-time.gap');
        const telDriver1 = document.querySelector('.tel-trace-driver1');

        // Elements for EduAgro (Lot tabs switch)
        const eduTabs = document.querySelectorAll('.edu-lot-tab');
        let currentEduTab = 0;

        // Elements for Pilates (Cama 6 toggle)
        const r6 = document.querySelector('.pcg-reformer.pulse-target');
        const pcgAvail = document.querySelector('.pcg-avail');
        let r6Reserved = false;

        simInterval = setInterval(() => {
            if (!simulationActive) return;

            // 1. Opportunity: Cycle through real OS pipeline stages
            if (oppTabs.length > 0) {
                oppTabs.forEach(t => t.classList.remove('active'));
                currentOppTab = (currentOppTab + 1) % oppTabs.length;
                oppTabs[currentOppTab].classList.add('active');
            }

            // 2. Club DRS: Countdown seconds tick down
            if (cdSec) {
                secCounter = secCounter > 0 ? secCounter - 1 : 59;
                cdSec.textContent = String(secCounter).padStart(2, '0');
            }

            // 3. DRS Telemetry: live gap jitter
            if (telGap) {
                const gaps = ['+0.248s', '+0.252s', '+0.245s', '+0.256s'];
                telGap.textContent = gaps[Math.floor(Math.random() * gaps.length)];
            }

            // 4. EduAgro: Cycle through fields
            if (eduTabs.length > 0) {
                eduTabs.forEach(t => t.classList.remove('active'));
                currentEduTab = (currentEduTab + 1) % eduTabs.length;
                eduTabs[currentEduTab].classList.add('active');
            }

            // 5. Pilates: live booking toggling
            if (r6 && pcgAvail) {
                r6Reserved = !r6Reserved;
                if (r6Reserved) {
                    r6.className = 'pcg-reformer occupied';
                    r6.innerHTML = '<span class="r-dot">●</span> Cama 6';
                    pcgAvail.innerHTML = '<strong>0 libres</strong> (Clase Llena)';
                } else {
                    r6.className = 'pcg-reformer available pulse-target';
                    r6.innerHTML = '<span class="r-dot">○</span> Cama 6';
                    pcgAvail.innerHTML = '<strong>1 libre</strong> de 6 camas';
                }
            }

        }, 2400);
    }

    function stopMicroSimulations() {
        simulationActive = false;
        if (simInterval) {
            clearInterval(simInterval);
            simInterval = null;
        }
    }
});
