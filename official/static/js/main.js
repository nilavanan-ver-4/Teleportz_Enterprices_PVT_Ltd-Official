document.addEventListener('DOMContentLoaded', () => {
    // High-End Mobile Sidebar Toggle
    const mobileLinkToggle = document.querySelector('.mobile-nav-toggle');
    const sidebarClose = document.querySelector('.sidebar-close');
    const sidebar = document.querySelector('.mobile-sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const body = document.body;

    const toggleSidebar = (forceClose = false) => {
        const isOpen = sidebar.classList.contains('active');
        if (forceClose || isOpen) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            mobileLinkToggle.classList.remove('active');
            body.style.overflow = '';
        } else {
            sidebar.classList.add('active');
            overlay.classList.add('active');
            mobileLinkToggle.classList.add('active');
            body.style.overflow = 'hidden';
        }
    };

    if (mobileLinkToggle) {
        mobileLinkToggle.addEventListener('click', () => toggleSidebar());
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', () => toggleSidebar(true));
    }

    if (overlay) {
        overlay.addEventListener('click', () => toggleSidebar(true));
    }

    // Close on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            toggleSidebar(true);
        }
    });

    // Close on link click (for same-page anchors)
    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => toggleSidebar(true));
    });

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

    // Scroller helper (use .parallax container when present) and Simple Parallax Effect
    const scroller = document.querySelector('.parallax') || window;
    const isWindowScroller = (scroller === window);
    const getScrollTop = () => isWindowScroller ? (window.pageYOffset || document.documentElement.scrollTop) : scroller.scrollTop;
    const getScrollHeight = () => isWindowScroller ? document.documentElement.scrollHeight : scroller.scrollHeight;
    const getInnerHeight = () => window.innerHeight;
    const scrollToY = (y) => {
        if (isWindowScroller) {
            window.scrollTo({ top: y, behavior: 'smooth' });
        } else {
            scroller.scrollTo({ top: y, behavior: 'smooth' });
        }
    };

    const handleParallax = () => {
        const scrolled = getScrollTop();
        const scrollHeight = getScrollHeight();
        const innerHeight = getInnerHeight();
        const maxScroll = scrollHeight - innerHeight;

        // Background & Layer Parallax
        document.querySelectorAll('.parallax-bg').forEach(bg => {
            const speed = 0.5;
            bg.style.transform = `translateY(${scrolled * speed}px)`;
        });

        document.querySelectorAll('.floating-layer').forEach(layer => {
            const speed = layer.dataset.speed || 0.2;
            layer.style.transform = `translateY(-${scrolled * speed}px)`;
        });

        // Footer & Navbar Scroll Parallax
        const airplane = document.getElementById('parallax-airplane');
        const sailboat = document.getElementById('parallax-sailboat');
        const navPlane = document.getElementById('navbar-airplane');

        if (airplane || sailboat || navPlane) {
            // Calculate scroll ratio (0 to 1)
            const ratio = Math.min(1, Math.max(0, scrolled / maxScroll));

            if (airplane) {
                // Airplane moves Forward (Left to Right)
                // Range: -10vw to 110vw
                const planeX = -10 + (ratio * 120);
                airplane.style.transform = `translateX(${planeX}vw) rotate(5deg)`;
            }

            if (navPlane) {
                // Navbar Airplane moves Forward (Left to Right)
                // Faster than footer for immediate impact
                const nPlaneX = -10 + (ratio * 150);
                navPlane.style.transform = `translateX(${nPlaneX}vw) rotate(-5deg)`;
            }

            if (sailboat) {
                // Sailboat moves Backward (Right to Left)
                // Range: 110vw to -10vw
                const shipX = 110 - (ratio * 120);
                // We flip the sailboat icon so it faces left (scaleX(-1))
                sailboat.style.transform = `translateX(${shipX}vw) translateY(${Math.sin(ratio * 20) * 5}px) scaleX(-1)`;
            }
        }
    };

    if (isWindowScroller) {
        window.addEventListener('scroll', handleParallax, { passive: true });
    } else {
        scroller.addEventListener('scroll', handleParallax, { passive: true });
    }
    handleParallax();

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

    // Live product search (realtime rendering)
    (function () {
        const searchInput = document.getElementById('product-search');
        const searchForm = document.getElementById('product-search-form');
        const statusEl = document.getElementById('product-search-status');
        const productsGrid = document.getElementById('products-grid');

        // simple debounce
        const debounce = (fn, wait = 250) => {
            let t = null;
            return function (...args) {
                clearTimeout(t);
                t = setTimeout(() => fn.apply(this, args), wait);
            };
        };

        const escapeHtml = (str) => {
            return String(str).replace(/[&<>"']/g, function (s) {
                return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": "&#39;" })[s];
            });
        };

        const renderProducts = (items) => {
            if (!productsGrid) return;
            if (!items || !items.length) {
                productsGrid.innerHTML = '<div class="text-center" style="grid-column: 1 / -1;"><p>No matching products found.</p></div>';
                return;
            }

            productsGrid.innerHTML = items.map(p => {
                const img = p.image_url ?
                    `<img src="${p.image_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1;">` :
                    `<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); z-index: 1;"></div>`;

                return `
                    <div class="bento-card product-item" 
                         data-name="${escapeHtml(p.name)}"
                         data-category="${escapeHtml(p.category)}"
                         data-description="${escapeHtml(p.description)}"
                         data-image="${p.image_url || ''}"
                         data-contact-url="/contact?subject=Inquiry: ${encodeURIComponent(p.name)}"
                         style="padding: 0; min-height: 420px; border-radius: 24px; cursor: pointer;">
                        ${img}
                        <div class="product-overlay">
                            <span class="product-category">${escapeHtml(p.category)}</span>
                            <div class="product-meta">
                                <h3 class="product-name">${escapeHtml(p.name)}</h3>
                                <!-- Description removed for cleaner search results -->
                            </div>
                            <div class="product-footer">
                                <button class="btn-product-view">View Details</button>
                                <button class="btn btn-primary product-inquire">
                                    Inquire
                                </button>
                            </div>
                        </div>
                    </div>`;
            }).join('');
        };

        const doSearch = debounce(async (e) => {
            const q = e.target.value.trim();
            if (statusEl) { statusEl.style.display = q ? 'block' : 'none'; statusEl.textContent = q ? 'Searching...' : ''; }
            try {
                const res = await fetch('/api/products?search=' + encodeURIComponent(q));
                if (!res.ok) throw new Error('Network');
                const data = await res.json();
                renderProducts(data);
            } catch (err) {
                console.error('Product search failed', err);
            } finally {
                if (statusEl) { statusEl.style.display = 'none'; }
            }
        }, 300);

        if (searchInput) {
            searchInput.addEventListener('input', doSearch);
            // prevent full page submit when JS active
            if (searchForm) searchForm.addEventListener('submit', (evt) => { evt.preventDefault(); });
        }
    })();

    // Downward Indicator Click - Smooth Scroll Down
    const downwardIndicator = document.querySelector('.downward-indicator');
    if (downwardIndicator) {
        // Ensure the element is accessible/focusable without changing template
        if (!downwardIndicator.hasAttribute('role')) downwardIndicator.setAttribute('role', 'button');
        if (!downwardIndicator.hasAttribute('tabindex')) downwardIndicator.setAttribute('tabindex', '0');
        if (!downwardIndicator.hasAttribute('aria-label')) downwardIndicator.setAttribute('aria-label', 'Scroll down');

        // Insert tiny delay to check Font Awesome rendering; if icon is not visible, add an SVG fallback
        const iconI = downwardIndicator.querySelector('i');
        const addFallbackIfNeeded = () => {
            try {
                if (iconI && iconI.getBoundingClientRect().width < 6) {
                    // hide the FA <i> visually but keep for semantics
                    iconI.style.display = 'none';
                    if (!downwardIndicator.querySelector('svg.fallback-icon')) {
                        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                        svg.setAttribute('class', 'fallback-icon');
                        svg.setAttribute('viewBox', '0 0 24 24');
                        svg.setAttribute('aria-hidden', 'true');
                        svg.innerHTML = '<path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
                        downwardIndicator.insertBefore(svg, downwardIndicator.firstChild);
                    }
                }
            } catch (e) {
                // ignore
            }
        };

        setTimeout(addFallbackIfNeeded, 300);

        const scrollDownToTarget = () => {
            // 1) explicit target selector (data-target)
            const targetSelector = downwardIndicator.dataset.target;
            if (targetSelector) {
                const targetEl = document.querySelector(targetSelector);
                if (targetEl) {
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }
            }

            // 2) data-next selector: sequentially advance through elements matching this selector on each click
            const nextSel = downwardIndicator.dataset.next || downwardIndicator.dataset.nextSelector;
            if (nextSel) {
                const matches = Array.from(document.querySelectorAll(nextSel));
                if (matches.length) {
                    // initialize pointer if not present or selector changed
                    if (typeof downwardIndicator._nextIndex === 'undefined' || downwardIndicator._nextSelector !== nextSel) {
                        downwardIndicator._nextIndex = 0;
                        downwardIndicator._nextSelector = nextSel;
                    }

                    // Ensure pointer is within bounds
                    let idx = downwardIndicator._nextIndex % matches.length;
                    if (idx < 0) idx = 0;

                    const targetEl = matches[idx];
                    if (targetEl) {
                        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        // advance pointer for the next click
                        downwardIndicator._nextIndex = (idx + 1) % matches.length;
                        return;
                    }
                }
            }

            // 2.5) If the indicator is inside a block, try to move to its next sibling block (reliable for parallax groups)
            const currentBlock = downwardIndicator.closest('section, .parallax-group, .content-group, .container');
            if (currentBlock) {
                let nextBlock = currentBlock.nextElementSibling;
                while (nextBlock && !nextBlock.matches('section, .parallax-group, .content-group, .container')) {
                    nextBlock = nextBlock.nextElementSibling;
                }
                if (nextBlock) {
                    nextBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }
            }

            // 3) fallback: next major block inside <main>
            const main = document.querySelector('main');
            if (main) {
                const candidates = Array.from(main.querySelectorAll('section, .container, .content-group, .parallax-group'));
                const found = candidates.find(el => {
                    const rect = el.getBoundingClientRect();
                    return rect.top > 64;
                });
                if (found) {
                    found.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }
            }

            // 4) fallback: scroll by configurable number of viewports (data-step, default 2)
            const maxScroll = getScrollHeight() - getInnerHeight();
            const multiplier = Math.max(0.1, parseFloat(downwardIndicator.dataset.step) || 2);
            const step = Math.round(getInnerHeight() * multiplier);
            const targetY = Math.min(getScrollTop() + step, maxScroll);
            scrollToY(targetY);
        };

        downwardIndicator.addEventListener('click', (e) => {
            e.preventDefault();
            scrollDownToTarget();
        });

        downwardIndicator.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
                e.preventDefault();
                scrollDownToTarget();
            }
        });

        // Show indicator on short pages; hide when user scrolls down on taller pages
        const handleDownScroll = () => {
            const scrollPosition = getScrollTop();
            const longPage = getScrollHeight() > getInnerHeight() + 40;
            if (!longPage) {
                downwardIndicator.style.opacity = '0.95';
                downwardIndicator.style.pointerEvents = 'auto';
                return;
            }

            if (scrollPosition > getInnerHeight() * 0.3) {
                downwardIndicator.style.opacity = '0';
                downwardIndicator.style.pointerEvents = 'none';
            } else {
                downwardIndicator.style.opacity = '0.95';
                downwardIndicator.style.pointerEvents = 'auto';
            }
        };

        // attach scroll listener to scroller (window or .parallax)
        if (isWindowScroller) {
            window.addEventListener('scroll', handleDownScroll, { passive: true });
        } else {
            scroller.addEventListener('scroll', handleDownScroll, { passive: true });
        }

        // Run fallback check on resize too
        window.addEventListener('resize', () => setTimeout(addFallbackIfNeeded, 150));
        handleDownScroll();
    }

    // Upward Indicator Click - Smooth Scroll / Sequential Prev Navigation
    const upwardIndicator = document.querySelector('.upward-indicator');
    if (upwardIndicator) {
        // Ensure accessibility attributes
        if (!upwardIndicator.hasAttribute('role')) upwardIndicator.setAttribute('role', 'button');
        if (!upwardIndicator.hasAttribute('tabindex')) upwardIndicator.setAttribute('tabindex', '0');
        if (!upwardIndicator.hasAttribute('aria-label')) upwardIndicator.setAttribute('aria-label', 'Scroll up');

        const scrollUpToTarget = () => {
            // 1) explicit target selector
            const targetSelector = upwardIndicator.dataset.target;
            if (targetSelector) {
                const targetEl = document.querySelector(targetSelector);
                if (targetEl) {
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }
            }

            // 2) data-prev selector: sequentially find previous match relative to viewport
            const prevSel = upwardIndicator.dataset.prev || upwardIndicator.dataset.prevSelector;
            if (prevSel) {
                const matches = Array.from(document.querySelectorAll(prevSel));
                if (matches.length) {
                    // Find first match that is at or below the top of viewport
                    const currentTopThreshold = 64;
                    let currentIndex = matches.findIndex(el => {
                        const rect = el.getBoundingClientRect();
                        return rect.top >= currentTopThreshold;
                    });
                    if (currentIndex === -1) {
                        // If none are below viewport, start from end
                        currentIndex = matches.length;
                    }
                    let prevIndex = (currentIndex - 1 + matches.length) % matches.length;
                    const targetEl = matches[prevIndex];
                    if (targetEl) {
                        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        return;
                    }
                }
            }

            // 3) fallback: scroll up by configurable number of viewports (data-step, default 2)
            const multiplier = Math.max(0.1, parseFloat(upwardIndicator.dataset.step) || 2);
            const step = Math.round(getInnerHeight() * multiplier);
            const targetY = Math.max(getScrollTop() - step, 0);
            scrollToY(targetY);
        };

        upwardIndicator.addEventListener('click', (e) => {
            e.preventDefault();
            scrollUpToTarget();
        });

        // Keyboard accessibility (Enter or Space)
        upwardIndicator.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
                e.preventDefault();
                scrollUpToTarget();
            }
        });

        // Show indicator when user scrolls down past first viewport
        const handleUpScroll = () => {
            const scrollPosition = getScrollTop();
            if (scrollPosition > getInnerHeight() * 0.5) {
                upwardIndicator.classList.add('visible');
                upwardIndicator.style.pointerEvents = 'auto';
            } else {
                upwardIndicator.classList.remove('visible');
                upwardIndicator.style.pointerEvents = 'none';
            }
        };

        if (isWindowScroller) {
            window.addEventListener('scroll', handleUpScroll);
        } else {
            scroller.addEventListener('scroll', handleUpScroll);
        }
        window.addEventListener('resize', handleUpScroll);
        handleUpScroll();
    }

    // --- Trade Expert AI Chatbot Logic ---
    const chatbotFAB = document.querySelector('.chatbot-fab');
    const chatWindow = document.querySelector('.chat-window');
    const chatClose = document.querySelector('.chat-close');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    const notificationBadge = document.querySelector('.notification-badge');

    const toggleChat = () => {
        chatWindow.classList.toggle('active');
        chatbotFAB.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            notificationBadge.style.display = 'none';
            chatInput.focus();
        }
    };

    chatbotFAB.addEventListener('click', toggleChat);
    chatClose.addEventListener('click', toggleChat);

    const addMessage = (text, type) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const textSpan = document.createElement('span');
        textSpan.textContent = text;
        messageDiv.appendChild(textSpan);

        if (type === 'user' || type === 'expert') {
            const statusDiv = document.createElement('div');
            statusDiv.className = 'message-status';
            statusDiv.innerHTML = '<i class="fa-solid fa-check-double"></i>';
            messageDiv.appendChild(statusDiv);
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const getExpertResponse = (userText) => {
        const input = userText.toLowerCase();

        if (input.includes('shipping') || input.includes('delivery') || input.includes('logistics')) {
            return "We offer end-to-end logistics coordination via sea, air, and land. Are you looking for a specific freight quote?";
        }
        if (input.includes('customs') || input.includes('duty') || input.includes('regulation')) {
            return "Our compliance team handles all HS code classifications and customs documentation. Do you have a specific country of origin in mind?";
        }
        if (input.includes('sourcing') || input.includes('products') || input.includes('suppliers')) {
            return "We specialize in global sourcing from verified vendors. You can check our latest catalog in the 'Products' section or tell me what you need.";
        }
        if (input.includes('hello') || input.includes('hi')) {
            return "Hello! I'm the Teleportz Trade Expert. How can I help you navigate global markets today?";
        }
        if (input.includes('price') || input.includes('cost')) {
            return "Pricing depends on volume and destination. I recommend visiting our 'Contact' page to request a detailed quote.";
        }

        return "That's an interesting trade query. I'll need to check our current freight schedules and compliance data. Would you like to leave your email for a specialist to follow up?";
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        chatInput.value = '';

        setTimeout(() => {
            typingIndicator.style.display = 'none';
            const response = getExpertResponse(text);
            addMessage(response, 'expert');
        }, 1500 + Math.random() * 1000);
    });

    // --- Product Details Modal Logic ---
    const productModal = document.getElementById('productModal');
    const modalImg = document.getElementById('modalProductImage');
    const modalCategory = document.getElementById('modalProductCategory');
    const modalName = document.getElementById('modalProductName');
    const modalDesc = document.getElementById('modalProductDescription');
    const modalContactLink = document.getElementById('modalContactLink');
    const modalMailLink = document.getElementById('modalMailLink');

    window.openProductModal = (name, category, description, imageUrl, contactUrl) => {
        if (!productModal || !modalName || !modalDesc) return;

        modalName.textContent = name || '';
        if (modalCategory) modalCategory.textContent = category || '';

        if (description) {
            modalDesc.innerHTML = description.replace(/\n/g, '<br>');
        } else {
            modalDesc.textContent = '';
        }

        if (modalImg) modalImg.src = imageUrl || '';
        if (modalContactLink) modalContactLink.href = contactUrl || '#';

        // Dynamic mail link
        if (modalMailLink) {
            const mailSubject = encodeURIComponent(`Inquiry regarding ${name}`);
            const mailBody = encodeURIComponent(`Hello Teleportz Team,\n\nI am interested in learning more about the ${name}. Please provide more details.\n\nRegards,`);
            modalMailLink.href = `mailto:info@teleportz.com?subject=${mailSubject}&body=${mailBody}`;
        }

        productModal.classList.add('active');
        body.style.overflow = 'hidden';
    };

    window.closeProductModal = () => {
        if (!productModal) return;
        productModal.classList.remove('active');
        body.style.overflow = '';

        // Clear data after animation
        setTimeout(() => {
            if (modalImg) modalImg.src = '';
            if (modalName) modalName.textContent = '';
            if (modalDesc) modalDesc.textContent = '';
        }, 300);
    };

    // Global listener for Product Inquire buttons and card clicks
    document.addEventListener('click', (e) => {
        // Find if we clicked a product-item OR inside one
        const card = e.target.closest('.product-item');
        if (card && !e.target.closest('.product-modal-content')) {
            const data = card.dataset;
            openProductModal(
                data.name,
                data.category,
                data.description,
                data.image,
                data.contactUrl
            );
            return;
        }

        // Close modal on overlay click
        if (e.target === productModal) {
            closeProductModal();
        }
    });

    // Close on ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && productModal && productModal.classList.contains('active')) {
            closeProductModal();
        }
    });
});
