/**
 * Mobile-First JavaScript Enhancements for PM Tool
 * Provides touch-friendly interactions and mobile optimizations
 */

// Mobile detection and initialization
(function() {
    'use strict';
    
    // Mobile detection
    const isMobile = window.innerWidth <= 768;
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // Add mobile classes to body
    if (isMobile) {
        document.body.classList.add('is-mobile');
    }
    if (isTouch) {
        document.body.classList.add('is-touch');
    }
    
    // Enhanced touch event handling
    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;
    
    // Viewport height fix for mobile browsers
    function setViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    // Initialize on load and resize
    setViewportHeight();
    window.addEventListener('resize', setViewportHeight);
    
    // Prevent zoom on double tap for iOS
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
    
    // Enhanced drag and drop for mobile
    class MobileDragDrop {
        constructor() {
            this.draggedElement = null;
            this.isDragging = false;
            this.startPos = { x: 0, y: 0 };
            this.currentPos = { x: 0, y: 0 };
            this.dragThreshold = 10;
            this.longPressTimeout = null;
            this.init();
        }
        
        init() {
            if (!isTouch) return;
            
            document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
            document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
            document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
        }
        
        handleTouchStart(e) {
            const card = e.target.closest('.card[draggable="true"]');
            if (!card) return;
            
            this.draggedElement = card;
            const touch = e.touches[0];
            this.startPos = { x: touch.clientX, y: touch.clientY };
            this.currentPos = { x: touch.clientX, y: touch.clientY };
            touchStartTime = Date.now();
            
            // Long press to start drag
            this.longPressTimeout = setTimeout(() => {
                this.startDrag();
            }, 200);
        }
        
        handleTouchMove(e) {
            if (!this.draggedElement) return;
            
            const touch = e.touches[0];
            this.currentPos = { x: touch.clientX, y: touch.clientY };
            
            const deltaX = this.currentPos.x - this.startPos.x;
            const deltaY = this.currentPos.y - this.startPos.y;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            if (distance > this.dragThreshold) {
                clearTimeout(this.longPressTimeout);
                
                if (!this.isDragging) {
                    this.startDrag();
                }
                
                if (this.isDragging) {
                    e.preventDefault();
                    this.updateDragPosition(deltaX, deltaY);
                    this.highlightDropZone(touch.clientX, touch.clientY);
                }
            }
        }
        
        handleTouchEnd(e) {
            clearTimeout(this.longPressTimeout);
            
            if (this.isDragging) {
                const touch = e.changedTouches[0];
                this.handleDrop(touch.clientX, touch.clientY);
            }
            
            this.resetDrag();
        }
        
        startDrag() {
            if (!this.draggedElement) return;
            
            this.isDragging = true;
            this.draggedElement.classList.add('dragging');
            this.draggedElement.style.zIndex = '1000';
            this.draggedElement.style.transition = 'none';
            
            // Add visual feedback
            this.addDragFeedback();
        }
        
        updateDragPosition(deltaX, deltaY) {
            if (!this.draggedElement) return;
            
            this.draggedElement.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
            this.draggedElement.style.opacity = '0.8';
        }
        
        highlightDropZone(x, y) {
            const elementBelow = document.elementFromPoint(x, y);
            const column = elementBelow?.closest('.column');
            
            // Remove previous highlights
            document.querySelectorAll('.column').forEach(col => {
                col.classList.remove('drag-target');
            });
            
            // Highlight current drop zone
            if (column && column !== this.draggedElement.closest('.column')) {
                column.classList.add('drag-target');
            }
        }
        
        handleDrop(x, y) {
            if (!this.draggedElement) return;
            
            const elementBelow = document.elementFromPoint(x, y);
            const targetColumn = elementBelow?.closest('.column');
            
            if (targetColumn && targetColumn !== this.draggedElement.closest('.column')) {
                const newStatus = targetColumn.dataset.status;
                const cardId = parseInt(this.draggedElement.dataset.cardId);
                
                // Move card visually
                targetColumn.querySelector('.cards-container').appendChild(this.draggedElement);
                
                // Update server if API is available
                this.updateCardStatus(cardId, newStatus);
                
                // Show success feedback
                this.showMoveSuccess();
            }
        }
        
        resetDrag() {
            if (this.draggedElement) {
                this.draggedElement.classList.remove('dragging');
                this.draggedElement.style.transform = '';
                this.draggedElement.style.opacity = '';
                this.draggedElement.style.zIndex = '';
                this.draggedElement.style.transition = '';
            }
            
            // Remove highlights
            document.querySelectorAll('.column').forEach(col => {
                col.classList.remove('drag-target');
            });
            
            this.removeDragFeedback();
            this.draggedElement = null;
            this.isDragging = false;
        }
        
        addDragFeedback() {
            const feedback = document.createElement('div');
            feedback.className = 'drag-feedback';
            feedback.innerHTML = '📱 Drag to move between columns';
            feedback.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 121, 191, 0.9);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                z-index: 10000;
                animation: fadeIn 0.3s ease-out;
            `;
            document.body.appendChild(feedback);
        }
        
        removeDragFeedback() {
            const feedback = document.querySelector('.drag-feedback');
            if (feedback) {
                feedback.remove();
            }
        }
        
        showMoveSuccess() {
            const success = document.createElement('div');
            success.innerHTML = '✅ Card moved successfully!';
            success.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: #36b37e;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                z-index: 10000;
                animation: slideDown 0.3s ease-out;
            `;
            document.body.appendChild(success);
            
            setTimeout(() => {
                success.style.animation = 'slideUp 0.3s ease-out';
                setTimeout(() => success.remove(), 300);
            }, 2000);
        }
        
        async updateCardStatus(cardId, status) {
            try {
                if (typeof fetch !== 'undefined' && window.location.pathname !== '/mobile-demo') {
                    await fetch('/api/move_card', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ card_id: cardId, status: status })
                    });
                }
                
                // Update column counts
                if (typeof updateColumnCounts === 'function') {
                    updateColumnCounts();
                }
            } catch (error) {
                console.error('Error updating card status:', error);
            }
        }
    }
    
    // Swipe gesture handler
    class SwipeHandler {
        constructor() {
            this.init();
        }
        
        init() {
            if (!isTouch) return;
            
            let startX = 0;
            let startY = 0;
            
            document.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            }, { passive: true });
            
            document.addEventListener('touchend', (e) => {
                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                
                const deltaX = endX - startX;
                const deltaY = endY - startY;
                
                // Horizontal swipe
                if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                    if (deltaX > 0) {
                        this.handleSwipeRight();
                    } else {
                        this.handleSwipeLeft();
                    }
                }
            }, { passive: true });
        }
        
        handleSwipeLeft() {
            // Close mobile nav if open
            const navLinks = document.getElementById('navLinks');
            if (navLinks && navLinks.classList.contains('mobile-open')) {
                navLinks.classList.remove('mobile-open');
                const icon = document.getElementById('mobileNavIcon');
                if (icon) icon.textContent = '☰';
            }
        }
        
        handleSwipeRight() {
            // Open mobile nav if closed (only on mobile)
            if (window.innerWidth <= 768) {
                const navLinks = document.getElementById('navLinks');
                const icon = document.getElementById('mobileNavIcon');
                if (navLinks && !navLinks.classList.contains('mobile-open')) {
                    navLinks.classList.add('mobile-open');
                    if (icon) icon.textContent = '✕';
                }
            }
        }
    }
    
    // Performance optimizations
    class PerformanceOptimizer {
        constructor() {
            this.init();
        }
        
        init() {
            // Lazy load images
            this.setupLazyLoading();
            
            // Optimize scrolling
            this.optimizeScrolling();
            
            // Preload critical resources
            this.preloadCriticalResources();
        }
        
        setupLazyLoading() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.classList.add('loaded');
                            imageObserver.unobserve(img);
                        }
                    });
                });
                
                document.querySelectorAll('img[data-src]').forEach(img => {
                    imageObserver.observe(img);
                });
            }
        }
        
        optimizeScrolling() {
            // Add smooth scrolling class to scrollable elements
            document.querySelectorAll('.board, .table-container, .notification-dropdown').forEach(el => {
                el.classList.add('smooth-scroll');
            });
        }
        
        preloadCriticalResources() {
            // Preload critical CSS and JS
            const criticalResources = [
                '/static/css/mobile-responsive.css'
            ];
            
            criticalResources.forEach(resource => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.href = resource;
                link.as = resource.endsWith('.css') ? 'style' : 'script';
                document.head.appendChild(link);
            });
        }
    }
    
    // Initialize all mobile enhancements
    document.addEventListener('DOMContentLoaded', () => {
        new MobileDragDrop();
        new SwipeHandler();
        new PerformanceOptimizer();
        
        // Add mobile-specific styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideDown {
                from { opacity: 0; transform: translate(-50%, -20px); }
                to { opacity: 1; transform: translate(-50%, 0); }
            }
            
            @keyframes slideUp {
                from { opacity: 1; transform: translate(-50%, 0); }
                to { opacity: 0; transform: translate(-50%, -20px); }
            }
            
            .is-mobile .card {
                min-height: 44px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .is-touch button, .is-touch .btn, .is-touch a {
                min-height: 44px;
                min-width: 44px;
            }
        `;
        document.head.appendChild(style);
    });
    
})();