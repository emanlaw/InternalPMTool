# Enhanced Dark Mode Implementation

## Overview

This document describes the comprehensive dark mode implementation for the PM Tool, which includes better contrast, system theme detection, multiple contrast levels, and full WCAG 2.1 AA/AAA compliance.

## Features Implemented

### 1. Color Specifications
- **Background**: `#1a1a1a` (very dark gray, not pure black)
- **Text**: `#f5f5f5` (very bright light gray)
- **Headers**: `#ffffff` (pure white for maximum readability)
- **Links**: `#64b5f6` (very bright blue for high visibility)
- **Cards/Panels**: `#2d2d2d` (dark gray with high contrast text)

### 2. Theme System Architecture

#### CSS Custom Properties
The implementation uses CSS custom properties (CSS variables) defined at the `:root` level for consistent theming:

```css
:root {
    /* Light Theme Colors */
    --bg-primary: #f4f5f7;
    --bg-secondary: #ffffff;
    --bg-tertiary: #ebecf0;
    --text-primary: #172b4d;
    --text-secondary: #5e6c84;
    --header-bg: #0079bf;
    --link-color: #0079bf;
    /* ... */
}

:root.dark-mode {
    /* Dark Theme Colors */
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-tertiary: #374151;
    --text-primary: #ffffff;
    --text-secondary: #f5f5f5;
    --link-color: #64b5f6;
    /* ... */
}

:root.high-contrast {
    /* High Contrast Theme */
    --bg-primary: #000000;
    --bg-secondary: #1a1a1a;
    --text-primary: #ffffff;
    --link-color: #00d4ff;
    /* ... */
}
```

#### Theme Manager JavaScript Class
The `ThemeManager` class handles all theme-related functionality:

```javascript
class ThemeManager {
    constructor() {
        this.themes = {
            light: 'light',
            dark: 'dark-mode',
            highContrast: 'high-contrast'
        };
        this.init();
    }
    
    // System theme detection
    detectSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.setTheme(this.themes.dark);
        } else {
            this.setTheme(this.themes.light);
        }
    }
    
    // Theme switching with localStorage persistence
    setTheme(theme) {
        // Remove all theme classes
        Object.values(this.themes).forEach(t => {
            document.documentElement.classList.remove(t);
            document.body.classList.remove(t);
        });
        
        // Add new theme class
        if (theme !== this.themes.light) {
            document.documentElement.classList.add(theme);
            document.body.classList.add(theme);
        }
        
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        this.updateIcons();
    }
}
```

### 3. User Interface Controls

#### Theme Toggle Buttons
Two buttons are provided in the header:
- **Dark Mode Toggle**: Switches between light and dark themes
- **Contrast Toggle**: Switches to high contrast mode

```html
<div class="theme-controls">
    <button onclick="toggleContrast()" class="contrast-toggle" title="Toggle High Contrast">
        <span id="contrastIcon">🔆</span>
    </button>
    <button onclick="toggleDarkMode()" class="dark-mode-toggle" title="Toggle Dark Mode">
        <span id="darkModeIcon">🌙</span>
    </button>
</div>
```

### 4. System Integration

#### OS Theme Detection
The system automatically detects and respects the user's operating system theme preference:

```javascript
// Listen for system theme changes
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            this.detectSystemTheme();
        }
    });
}
```

#### Preference Persistence
User theme preferences are saved in localStorage and restored on page load.

### 5. Accessibility Compliance

#### WCAG 2.1 Contrast Ratios
All color combinations meet or exceed WCAG guidelines:

| Theme | Text Type | Background | Foreground | Ratio | Standard |
|-------|-----------|------------|------------|-------|----------|
| Light | Primary | #f4f5f7 | #172b4d | 12.93:1 | AAA |
| Light | Secondary | #ffffff | #5e6c84 | 5.31:1 | AA |
| Light | Links | #ffffff | #0079bf | 4.68:1 | AA |
| Dark | Headers | #1a1a1a | #ffffff | 17.40:1 | AAA |
| Dark | Primary | #1a1a1a | #f5f5f5 | 15.96:1 | AAA |
| Dark | Cards | #2d2d2d | #ffffff | 13.77:1 | AAA |
| Dark | Links | #1a1a1a | #64b5f6 | 7.86:1 | AAA |
| High Contrast | Primary | #000000 | #ffffff | 21.00:1 | AAA |
| High Contrast | Links | #000000 | #00d4ff | 11.86:1 | AAA |

#### Smooth Transitions
All theme-related properties include smooth 0.3s ease transitions to reduce jarring visual changes:

```css
* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
```

### 6. Cross-File Implementation

#### Updated CSS Files
All CSS files have been updated to use the new system:

1. **templates/base.html**: Core theme system and CSS custom properties
2. **static/css/sprints.css**: Sprint management pages
3. **static/css/mindmap.css**: Mind map functionality
4. **static/css/registration.css**: User registration pages
5. **static/css/gantt_analytics.css**: Analytics and Gantt chart pages

#### Implementation Pattern
Each CSS file follows the same pattern:

```css
/* Remove old .dark-mode selectors */
/* Add CSS custom property usage */
.component {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border-color: var(--border-color);
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
```

## Usage

### For Users
1. **Dark Mode Toggle**: Click the moon/sun icon in the header to toggle between light and dark themes
2. **High Contrast**: Click the brightness icon to enable high contrast mode for better accessibility
3. **System Integration**: The theme will automatically match your OS preference if no manual selection is made

### For Developers
1. **Adding New Components**: Use CSS custom properties instead of hardcoded colors
2. **Theme-Aware Styling**: Always include the transition property for smooth theme changes
3. **Testing**: Use the provided contrast testing tool to verify WCAG compliance

```css
/* Good - Uses custom properties */
.new-component {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

/* Bad - Hardcoded colors */
.new-component {
    background: #ffffff;
    color: #000000;
}
```

## Technical Benefits

1. **Maintainability**: CSS custom properties centralize color management
2. **Performance**: Smooth transitions without layout thrashing
3. **Accessibility**: Exceeds WCAG requirements for all user groups
4. **User Experience**: Respects system preferences and user choices
5. **Future-Proof**: Easy to add new themes or modify existing ones

## Testing

The implementation includes a comprehensive contrast testing tool that validates all color combinations against WCAG 2.1 standards. All combinations achieve AA or AAA compliance levels.

## Browser Support

- **CSS Custom Properties**: Supported in all modern browsers
- **prefers-color-scheme**: Supported in all modern browsers
- **localStorage**: Universally supported
- **Graceful Degradation**: Falls back to light theme on older browsers

## Conclusion

This enhanced dark mode implementation provides a comprehensive, accessible, and user-friendly theming system that meets all specified requirements while maintaining excellent code quality and performance.