document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu
    const mobileMenuBtn = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.backgroundColor = 'rgba(15, 23, 42, 0.95)';
                navLinks.style.padding = '2rem';
                navLinks.style.backdropFilter = 'blur(10px)';
            }
        });
    }

    // Scroll Reveal
    const revealElements = document.querySelectorAll('.scroll-reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => revealObserver.observe(el));

    // Simple Parallax Effect (JS fallback/enhancement)
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        document.querySelectorAll('.parallax-bg').forEach(bg => {
            const speed = 0.5;
            bg.style.transform = `translateY(${scrolled * speed}px)`;
        });

        document.querySelectorAll('.floating-layer').forEach(layer => {
            const speed = layer.dataset.speed || 0.2;
            layer.style.transform = `translateY(-${scrolled * speed}px)`;
        });
    });

    // Tilt Effect for Cards
    document.querySelectorAll('.bento-card, .hero-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Reduced rotation for subtle premium feel
            const rotateX = (centerY - y) / 40;
            const rotateY = (x - centerX) / 40;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.01)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });

    // Mouse Parallax for Background (Interactive Depth)
    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth - e.pageX * 2) / 100;
        const y = (window.innerHeight - e.pageY * 2) / 100;

        document.querySelectorAll('.parallax-layer--back').forEach(layer => {
            // Apply slight offset based on mouse position
            // We use existing transform logic so we need to be careful not to override translateZ
            // But CSS transform is static, we can add a custom property or modify the transform string.
            // Simpler approach: shift background-position or use a child element. 
            // Better: Translate the layer slightly.
            // Since it already has translateZ, we must maintain it.
            layer.style.transform = `translateZ(-1px) scale(2.05) translate(${x}px, ${y}px)`;
        });
    });

    // Downward Indicator Click - Smooth Scroll Down
    const downwardIndicator = document.querySelector('.downward-indicator');
    if (downwardIndicator) {
        downwardIndicator.addEventListener('click', () => {
            // Scroll down by one viewport height
            const parallaxWrapper = document.querySelector('.parallax-wrapper');
            if (parallaxWrapper) {
                parallaxWrapper.scrollBy({
                    top: window.innerHeight,
                    behavior: 'smooth'
                });
            }
        });

        // Hide indicator when user scrolls past first viewport
        const parallaxWrapper = document.querySelector('.parallax-wrapper');
        if (parallaxWrapper) {
            parallaxWrapper.addEventListener('scroll', () => {
                const scrollPosition = parallaxWrapper.scrollTop;
                if (scrollPosition > window.innerHeight * 0.3) {
                    downwardIndicator.style.opacity = '0';
                    downwardIndicator.style.pointerEvents = 'none';
                } else {
                    downwardIndicator.style.opacity = '0.8';
                    downwardIndicator.style.pointerEvents = 'auto';
                }
            });
        }
    }

    // Upward Indicator Click - Smooth Scroll to Top
    const upwardIndicator = document.querySelector('.upward-indicator');
    if (upwardIndicator) {
        upwardIndicator.addEventListener('click', () => {
            // Scroll to top of page
            const parallaxWrapper = document.querySelector('.parallax-wrapper');
            if (parallaxWrapper) {
                parallaxWrapper.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });

        // Show indicator when user scrolls down past first viewport
        const parallaxWrapper = document.querySelector('.parallax-wrapper');
        if (parallaxWrapper) {
            parallaxWrapper.addEventListener('scroll', () => {
                const scrollPosition = parallaxWrapper.scrollTop;
                if (scrollPosition > window.innerHeight * 0.5) {
                    upwardIndicator.classList.add('visible');
                } else {
                    upwardIndicator.classList.remove('visible');
                }
            });
        }
    }
});
