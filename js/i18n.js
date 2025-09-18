// Internationalization (i18n) System for Library Management System

class I18n {
    constructor() {
        this.currentLanguage = 'ar'; // Default to Arabic
        this.translations = {};
        this.isRTL = false;
        
        this.init();
    }

    async init() {
        // Load saved language preference or use default
        const savedLang = localStorage.getItem('lms_language') || 'ar';
        await this.loadLanguage(savedLang);
        this.setupLanguageToggle();
    }

    async loadLanguage(lang) {
        try {
            const response = await fetch(`js/languages/${lang}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load language file: ${lang}`);
            }
            
            this.translations = await response.json();
            this.currentLanguage = lang;
            this.isRTL = lang === 'ar';
            
            // Save preference
            localStorage.setItem('lms_language', lang);
            
            // Apply translations and layout
            this.applyTranslations();
            this.applyRTLLayout();
            this.updateLanguageToggle();
            
        } catch (error) {
            console.error('Error loading language:', error);
            // Fallback to English if Arabic fails
            if (lang === 'ar') {
                await this.loadLanguage('en');
            }
        }
    }

    setupLanguageToggle() {
        const languageDropdown = document.getElementById('language-dropdown');
        if (languageDropdown) {
            languageDropdown.addEventListener('change', (e) => {
                const selectedLang = e.target.value;
                this.loadLanguage(selectedLang);
            });
        }
    }

    updateLanguageToggle() {
        const languageDropdown = document.getElementById('language-dropdown');
        if (languageDropdown) {
            languageDropdown.value = this.currentLanguage;
        }
    }

    applyTranslations() {
        // Translate elements with data-translate attribute
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        });

        // Translate placeholders
        const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            const translation = this.getTranslation(key);
            if (translation) {
                element.placeholder = translation;
            }
        });

        // Translate title attributes
        const titleElements = document.querySelectorAll('[data-translate-title]');
        titleElements.forEach(element => {
            const key = element.getAttribute('data-translate-title');
            const translation = this.getTranslation(key);
            if (translation) {
                element.title = translation;
            }
        });

        // Update document title
        const titleTranslation = this.getTranslation('app.title');
        if (titleTranslation) {
            document.title = titleTranslation;
        }
    }

    applyRTLLayout() {
        const html = document.documentElement;
        const body = document.body;
        
        // Keep LTR layout for both languages
        html.setAttribute('dir', 'ltr');
        
        if (this.isRTL) {
            html.setAttribute('lang', 'ar');
            body.classList.add('arabic-text');
        } else {
            html.setAttribute('lang', 'en');
            body.classList.remove('arabic-text');
        }
    }

    getTranslation(key) {
        const keys = key.split('.');
        let translation = this.translations;
        
        for (const k of keys) {
            if (translation && typeof translation === 'object' && k in translation) {
                translation = translation[k];
            } else {
                return null;
            }
        }
        
        return translation;
    }

    // Helper method to translate text dynamically
    t(key, params = {}) {
        let translation = this.getTranslation(key);
        
        if (!translation) {
            return key; // Return key if translation not found
        }
        
        // Replace parameters in translation
        Object.keys(params).forEach(param => {
            translation = translation.replace(`{${param}}`, params[param]);
        });
        
        return translation;
    }

    // Method to get current language
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Method to check if current language is RTL
    isCurrentLanguageRTL() {
        return this.isRTL;
    }
}

// Initialize i18n system
const i18n = new I18n();

// Make i18n available globally
window.i18n = i18n;
