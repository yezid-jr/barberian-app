import API from './utils/api.js';
import CONFIG from './config.js';

class App {
    constructor() {
        this.currentUser = null;
        this.currentPage = 'home';
        this.init();
    }

    init() {
        // Check if user is logged in
        this.checkAuthStatus();

        // Setup event listeners
        this.setupEventListeners();

        // Initial render
        this.renderNavigation();

        console.log('🚀 Barberian App started');
    }

    checkAuthStatus() {
        const token = API.getToken();
        const userData = localStorage.getItem(CONFIG.STORAGE.USER_KEY);

        if (token && userData) {
            try {
                this.currentUser = JSON.parse(userData);
                console.log('Authenticated user:', this.currentUser);
            } catch (error) {
                console.error('Error parsing user data:', error);
                API.removeToken();
            }
        }
    }

    setupEventListeners() {
        // Login/Register buttons on home
        document.getElementById('btn-login')?.addEventListener('click', () => {
            this.showLoginForm();
        });

        document.getElementById('btn-register')?.addEventListener('click', () => {
            this.showRegisterForm();
        });

        // Navegation links
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-page]')) {
                e.preventDefault();
                const page = e.target.getAttribute('data-page');
                this.navigateTo(page);
            }
        });
    }
    // Render navigation based on auth status
    renderNavigation() {
        const navMenu = document.getElementById('nav-menu');

        if (this.currentUser) {
            // User is logged in
            navMenu.innerHTML = `
                <span class="text-gray-700">Hi, ${this.currentUser.full_name}</span>
                <button data-page="profile" class="text-blue-600 hover:text-blue-800">My Profile</button>
                ${this.currentUser.role === 'admin' ?
                    '<button data-page="admin" class="text-purple-600 hover:text-purple-800">Admin</button>' :
                    ''
                }
                <button id="btn-logout" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded">
                    Logout
                </button>
            `;

            // Event listener for logout
            document.getElementById('btn-logout').addEventListener('click', () => {
                this.logout();
            });
        } else {
            // Usuario no logueado
            navMenu.innerHTML = `
                <button data-page="login" class="text-blue-600 hover:text-blue-800">Iniciar Sesión</button>
                <button data-page="register" class="text-green-600 hover:text-green-800">Registrarse</button>
            `;
        }
    }

    navigateTo(page) {
        this.currentPage = page;

        switch (page) {
            case 'login':
                this.showLoginForm();
                break;
            case 'register':
                this.showRegisterForm();
                break;
            case 'profile':
                this.showProfile();
                break;
            case 'admin':
                this.showAdminPanel();
                break;
            default:
                this.showHome();
        }
    }

    showHome() {
        const content = document.getElementById('content');

        if (this.currentUser) {
            content.innerHTML = `
                <div class="text-center py-20 fade-in">
                    <h2 class="text-3xl font-bold text-gray-800 mb-4">Bienvenido de vuelta, ${this.currentUser.full_name}!</h2>
                    <p class="text-gray-600 mb-8">¿Qué deseas hacer hoy?</p>
                    
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
                        ${this.currentUser.role === 'customer' ? `
                            <div class="card hover:shadow-lg transition-shadow cursor-pointer" data-page="appointments">
                                <h3 class="text-xl font-bold mb-2">Mis Citas</h3>
                                <p class="text-gray-600">Ver y gestionar tus citas</p>
                            </div>
                            <div class="card hover:shadow-lg transition-shadow cursor-pointer">
                                <h3 class="text-xl font-bold mb-2">Agendar Cita</h3>
                                <p class="text-gray-600">Reserva una nueva cita</p>
                            </div>
                        ` : ''}
                        
                        ${this.currentUser.role === 'admin' ? `
                            <div class="card hover:shadow-lg transition-shadow cursor-pointer" data-page="admin">
                                <h3 class="text-xl font-bold mb-2">Panel Admin</h3>
                                <p class="text-gray-600">Gestionar el sistema</p>
                            </div>
                        ` : ''}
                        
                        <div class="card hover:shadow-lg transition-shadow cursor-pointer" data-page="profile">
                            <h3 class="text-xl font-bold mb-2">Mi Perfil</h3>
                            <p class="text-gray-600">Ver y editar perfil</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            content.innerHTML = `
                <div class="text-center py-20">
                    <h2 class="text-3xl font-bold text-gray-800 mb-4">Bienvenido a Barberian</h2>
                    <p class="text-gray-600 mb-8">Sistema de gestión de barberías</p>
                    
                    <div class="space-x-4">
                        <button id="btn-login" class="btn-primary">
                            Iniciar Sesión
                        </button>
                        <button id="btn-register" class="btn-success">
                            Registrarse
                        </button>
                    </div>
                </div>
            `;

            this.setupEventListeners();
        }
    }

    showLoginForm() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-md mx-auto mt-20 fade-in">
                <div class="card">
                    <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Iniciar Sesión</h2>
                    
                    <!-- Botón de Google OAuth -->
                    <button 
                        id="googleLoginBtn" 
                        class="w-full bg-white border-2 border-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-50 transition duration-300 mb-4 flex items-center justify-center space-x-2"
                    >
                        <svg class="w-5 h-5" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        <span>Continuar con Google</span>
                    </button>
                
                    <!-- Separador -->
                    <div class="flex items-center justify-center my-4">
                        <div class="flex-grow border-t border-gray-300"></div>
                        <span class="flex-shrink mx-4 text-gray-600">o</span>
                        <div class="flex-grow border-t border-gray-300"></div>
                    </div>

                    <form id="login-form">
                        <div class="mb-4">
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" id="email" name="email" required 
                                   class="input-field" placeholder="tu@email.com">
                        </div>
                        
                        <div class="mb-6">
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
                            <input type="password" id="password" name="password" required 
                                   class="input-field" placeholder="********">
                        </div>
                        
                        <div id="login-error" class="hidden mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"></div>
                        
                        <button type="submit" class="w-full btn-primary mb-4">
                            Iniciar Sesión
                        </button>
                    </form>
                    
                    <div class="text-center">
                        <p class="text-sm text-gray-600">
                            ¿No tienes cuenta? 
                            <button data-page="register" class="text-blue-600 hover:text-blue-800 underline">
                                Regístrate aquí
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        `;

        // Event listener para el formulario de login
        document.getElementById('login-form').addEventListener('submit', (e) => {
            this.handleLogin(e);
        });
    }

    showRegisterForm() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-md mx-auto mt-20 fade-in">
                <div class="card">
                    <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Registrarse</h2>
                    
                    <form id="register-form">
                        <div class="mb-4">
                            <label for="full_name" class="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
                            <input type="text" id="full_name" name="full_name" required 
                                   class="input-field" placeholder="Juan Pérez">
                        </div>
                        
                        <div class="mb-4">
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" id="email" name="email" required 
                                   class="input-field" placeholder="tu@email.com">
                        </div>
                        
                        <div class="mb-4">
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
                            <input type="password" id="password" name="password" required 
                                   class="input-field" placeholder="********" minlength="6">
                        </div>
                        
                        <div class="mb-6">
                            <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-2">Confirmar Contraseña</label>
                            <input type="password" id="confirm_password" name="confirm_password" required 
                                   class="input-field" placeholder="********" minlength="6">
                        </div>
                        
                        <div id="register-error" class="hidden mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"></div>
                        <div id="register-success" class="hidden mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded"></div>
                        
                        <button type="submit" class="w-full btn-success mb-4">
                            Registrarse
                        </button>
                    </form>
                    
                    <div class="text-center">
                        <p class="text-sm text-gray-600">
                            ¿Ya tienes cuenta? 
                            <button data-page="login" class="text-blue-600 hover:text-blue-800 underline">
                                Inicia sesión aquí
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        `;

        // Event listener para el formulario de registro
        document.getElementById('register-form').addEventListener('submit', (e) => {
            this.handleRegister(e);
        });
    }

    async handleLogin(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const errorDiv = document.getElementById('login-error');
        const submitBtn = form.querySelector('button[type="submit"]');

        // Mostrar estado de carga
        submitBtn.disabled = true;
        submitBtn.textContent = 'Iniciando sesión...';
        errorDiv.classList.add('hidden');

        try {
            const credentials = {
                email: formData.get('email'),
                password: formData.get('password')
            };

            const response = await API.login(credentials);

            // Guardar datos del usuario
            API.saveToken(response.token);
            localStorage.setItem(CONFIG.STORAGE.USER_KEY, JSON.stringify(response.user));

            this.currentUser = response.user;

            // Actualizar la interfaz
            this.renderNavigation();
            this.showHome();

            console.log('Login exitoso:', response.user);

        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Iniciar Sesión';
        }
    }

    async handleRegister(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const errorDiv = document.getElementById('register-error');
        const successDiv = document.getElementById('register-success');
        const submitBtn = form.querySelector('button[type="submit"]');

        // Validar contraseñas
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');

        if (password !== confirmPassword) {
            errorDiv.textContent = 'Las contraseñas no coinciden';
            errorDiv.classList.remove('hidden');
            successDiv.classList.add('hidden');
            return;
        }

        // Mostrar estado de carga
        submitBtn.disabled = true;
        submitBtn.textContent = 'Registrando...';
        errorDiv.classList.add('hidden');
        successDiv.classList.add('hidden');

        try {
            const userData = {
                full_name: formData.get('full_name'),
                email: formData.get('email'),
                password: password
            };

            const response = await API.register(userData);

            successDiv.textContent = 'Registro exitoso! Ahora puedes iniciar sesión.';
            successDiv.classList.remove('hidden');

            // Limpiar formulario
            form.reset();

            // Redirigir al login después de 2 segundos
            setTimeout(() => {
                this.showLoginForm();
            }, 2000);

            console.log('Registro exitoso:', response);

        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Registrarse';
        }
    }

    showProfile() {
        if (!this.currentUser) {
            this.showLoginForm();
            return;
        }

        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-2xl mx-auto mt-10 fade-in">
                <div class="card">
                    <h2 class="text-2xl font-bold text-gray-800 mb-6">Mi Perfil</h2>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
                            <p class="text-gray-900">${this.currentUser.full_name}</p>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                            <p class="text-gray-900">${this.currentUser.email}</p>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
                            <p class="text-gray-900 capitalize">${this.currentUser.role}</p>
                        </div>
                    </div>
                    
                    <div class="mt-6 pt-6 border-t">
                        <button id="test-api" class="btn-primary mr-2">
                            Probar API Protegida
                        </button>
                        <button onclick="app.showHome()" class="btn-secondary">
                            Volver al Inicio
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Event listener para probar API
        document.getElementById('test-api').addEventListener('click', async () => {
            try {
                const response = await API.getProfile();
                alert('API funcionando: ' + JSON.stringify(response, null, 2));
            } catch (error) {
                alert('Error en API: ' + error.message);
            }
        });
    }

    showAdminPanel() {
        if (!this.currentUser || this.currentUser.role !== 'admin') {
            alert('Acceso denegado');
            this.showHome();
            return;
        }

        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto mt-10 fade-in">
                <div class="card">
                    <h2 class="text-2xl font-bold text-gray-800 mb-6">Panel de Administración</h2>
                    <p class="text-gray-600 mb-4">Funciones administrativas del sistema</p>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="p-4 border rounded-lg">
                            <h3 class="font-bold mb-2">Gestión de Usuarios</h3>
                            <p class="text-sm text-gray-600">Administrar usuarios del sistema</p>
                        </div>
                        
                        <div class="p-4 border rounded-lg">
                            <h3 class="font-bold mb-2">Gestión de Barberías</h3>
                            <p class="text-sm text-gray-600">Administrar barberías y ubicaciones</p>
                        </div>
                        
                        <div class="p-4 border rounded-lg">
                            <h3 class="font-bold mb-2">Reportes</h3>
                            <p class="text-sm text-gray-600">Ver estadísticas y reportes</p>
                        </div>
                        
                        <div class="p-4 border rounded-lg">
                            <h3 class="font-bold mb-2">Configuración</h3>
                            <p class="text-sm text-gray-600">Configurar parámetros del sistema</p>
                        </div>
                    </div>
                    
                    <div class="mt-6 pt-6 border-t">
                        <button onclick="app.showHome()" class="btn-secondary">
                            Volver al Inicio
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    logout() {
        API.removeToken();
        this.currentUser = null;
        this.renderNavigation();
        this.showHome();
        console.log('Usuario deslogueado');
    }
}

// Inicializar la aplicación
const app = new App();

// Hacer disponible globalmente para debugging
window.app = app;