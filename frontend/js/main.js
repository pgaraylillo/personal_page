// ===================================
// Configuration
// ===================================
const API_BASE_URL = '';

// ===================================
// Theme Management
// ===================================
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'dark';
        this.themeToggle = document.getElementById('themeToggle');
        this.init();
    }

    init() {
        this.applyTheme();
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        const icon = this.themeToggle.querySelector('i');
        icon.className = this.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    toggleTheme() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
    }
}

// ===================================
// Apps Management
// ===================================
class AppsManager {
    constructor() {
        this.appsGrid = document.getElementById('appsGrid');
        this.loadApps();
    }

    async loadApps() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/apps`);
            if (!response.ok) throw new Error('Failed to load apps');

            const apps = await response.json();
            this.renderApps(apps);

            // Update stats
            document.getElementById('projectsCount').textContent = apps.length;
            this.animateCounter('projectsCount', apps.length);
        } catch (error) {
            console.error('Error loading apps:', error);
            this.appsGrid.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-muted">Unable to load projects. Please try again later.</p>
                </div>
            `;
        }
    }

    renderApps(apps) {
        // Show featured apps first
        const sortedApps = apps.sort((a, b) => b.featured - a.featured);

        this.appsGrid.innerHTML = sortedApps.map(app => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="app-card">
                    <div class="app-image">
                        ${app.image_url ?
                `<img src="${app.image_url}" alt="${app.name}" style="width: 100%; height: 100%; object-fit: cover;">` :
                `<i class="fas fa-${this.getAppIcon(app.tech_stack)}"></i>`
            }
                    </div>
                    <div class="app-content">
                        <h3 class="app-title">${app.name}</h3>
                        <p class="app-description">${app.description}</p>
                        <div class="app-tech">
                            ${app.tech_stack.slice(0, 4).map(tech =>
                `<span class="tech-badge">${tech}</span>`
            ).join('')}
                        </div>
                        <div class="app-links">
                            ${app.demo_url ?
                `<a href="${app.demo_url}" target="_blank" rel="noopener" class="app-link app-link-primary">
                                    <i class="fas fa-external-link-alt me-1"></i> Demo
                                </a>` : ''}
                            ${app.github_url ?
                `<a href="${app.github_url}" target="_blank" rel="noopener" class="app-link app-link-secondary">
                                    <i class="fab fa-github me-1"></i> Code
                                </a>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    getAppIcon(techStack) {
        const icons = {
            'React': 'react',
            'Vue.js': 'vuejs',
            'Python': 'python',
            'FastAPI': 'bolt',
            'Docker': 'docker',
            'Node.js': 'node-js',
            'MongoDB': 'database',
            'PostgreSQL': 'database'
        };

        for (const tech of techStack) {
            if (icons[tech]) return icons[tech];
        }
        return 'code';
    }

    animateCounter(elementId, target) {
        const element = document.getElementById(elementId);
        let current = 0;
        const increment = target / 30;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }
}

// ===================================
// Blog Management
// ===================================
class BlogManager {
    constructor() {
        this.blogGrid = document.getElementById('blogGrid');

        // Modal elements
        this.modal = document.getElementById('blogModal');
        this.modalBackdrop = document.getElementById('blogModalBackdrop');
        this.modalClose = document.getElementById('blogModalClose');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalDate = document.getElementById('modalDate');
        this.modalAuthor = document.getElementById('modalAuthor');
        this.modalTags = document.getElementById('modalTags');
        this.modalBody = document.getElementById('modalBody');

        this.init();
        this.loadBlogPosts();
    }

    init() {
        // Modal event listeners
        this.modalClose.addEventListener('click', () => this.closeModal());
        this.modalBackdrop.addEventListener('click', () => this.closeModal());

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.closeModal();
            }
        });
    }

    async loadBlogPosts() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/blog`);
            if (!response.ok) throw new Error('Failed to load blog posts');

            const posts = await response.json();
            this.renderBlogPosts(posts);

            // Update stats
            document.getElementById('blogCount').textContent = posts.length;
            this.animateCounter('blogCount', posts.length);
        } catch (error) {
            console.error('Error loading blog posts:', error);
            this.blogGrid.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-muted">Unable to load blog posts. Please try again later.</p>
                </div>
            `;
        }
    }

    renderBlogPosts(posts) {
        this.blogGrid.innerHTML = posts.slice(0, 6).map(post => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="blog-card">
                    <div class="blog-meta">
                        <span><i class="far fa-calendar me-1"></i>${this.formatDate(post.date)}</span>
                        <span><i class="far fa-user me-1"></i>${post.author}</span>
                    </div>
                    <h3 class="blog-title">${post.title}</h3>
                    <p class="blog-excerpt">${post.excerpt}</p>
                    ${post.tags && post.tags.length > 0 ? `
                        <div class="blog-tags">
                            ${post.tags.map(tag => `<span class="tag-badge">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    <a href="#" class="read-more" data-slug="${post.slug}">
                        Read More <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        `).join('');

        // Add click handlers for "Read More" links
        document.querySelectorAll('.read-more').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.showBlogPost(e.target.closest('.read-more').dataset.slug);
            });
        });
    }

    async showBlogPost(slug) {
        this.openModal();
        this.setModalLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/blog/${slug}`);
            if (!response.ok) throw new Error('Failed to load blog post');

            const post = await response.json();
            this.renderModalContent(post);
        } catch (error) {
            console.error('Error loading blog post:', error);
            this.modalBody.innerHTML = `
                <div class="text-center text-danger">
                    <i class="fas fa-exclamation-circle fa-3x mb-3"></i>
                    <p>Error loading article. Please try again.</p>
                </div>
            `;
        } finally {
            this.setModalLoading(false);
        }
    }

    renderModalContent(post) {
        this.modalTitle.textContent = post.title;
        this.modalDate.innerHTML = `<i class="far fa-calendar me-1"></i>${this.formatDate(post.date)}`;
        this.modalAuthor.innerHTML = `<i class="far fa-user me-1"></i>${post.author}`;

        if (post.tags && post.tags.length > 0) {
            this.modalTags.innerHTML = post.tags.map(tag =>
                `<span class="tag-badge">${tag}</span>`
            ).join('');
        } else {
            this.modalTags.innerHTML = '';
        }

        this.modalBody.innerHTML = post.content;
    }

    setModalLoading(isLoading) {
        if (isLoading) {
            this.modalBody.innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            `;
            this.modalTitle.textContent = '';
            this.modalDate.textContent = '';
            this.modalAuthor.textContent = '';
            this.modalTags.innerHTML = '';
        }
    }

    openModal() {
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    closeModal() {
        this.modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    animateCounter(elementId, target) {
        const element = document.getElementById(elementId);
        let current = 0;
        const increment = target / 30;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }
}

// ===================================
// Chat Widget
// ===================================
class ChatWidget {
    constructor() {
        this.chatToggle = document.getElementById('chatToggle');
        this.chatWindow = document.getElementById('chatWindow');
        this.chatClose = document.getElementById('chatClose');
        this.chatInput = document.getElementById('chatInput');
        this.chatSend = document.getElementById('chatSend');
        this.chatMessages = document.getElementById('chatMessages');
        this.init();
    }

    init() {
        this.chatToggle.addEventListener('click', () => this.toggleChat());
        this.chatClose.addEventListener('click', () => this.closeChat());
        this.chatSend.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    toggleChat() {
        this.chatWindow.classList.toggle('active');
        if (this.chatWindow.classList.contains('active')) {
            this.chatInput.focus();
        }
    }

    closeChat() {
        this.chatWindow.classList.remove('active');
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.chatInput.value = '';

        // Disable input while waiting for response
        this.chatSend.disabled = true;
        this.chatInput.disabled = true;

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error('Failed to get response');

            const data = await response.json();
            this.addMessage(data.response, 'bot');
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
        } finally {
            this.chatSend.disabled = false;
            this.chatInput.disabled = false;
            this.chatInput.focus();
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// ===================================
// Smooth Scrolling
// ===================================
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href === '#' || !href) return;

                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 70; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
}

// ===================================
// Navbar Scroll Effect
// ===================================
class NavbarScroll {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                this.navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
            } else {
                this.navbar.style.boxShadow = 'none';
            }
        });
    }
}

// ===================================
// Initialize Everything
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new AppsManager();
    new BlogManager();
    new ChatWidget();
    new SmoothScroll();
    new NavbarScroll();
});
