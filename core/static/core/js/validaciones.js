// Funciones de validación
const validators = {
    email: email => /^[\w.-]+@[\w.-]+\.[a-z]{2,6}$/i.test(email),
    username: username => /^[\w]{4,20}$/.test(username),
    phone: phone => /^[+0-9]{8,15}$/.test(phone),
    password: pass => {
      const rules = [
        { test: pass.length >= 8, msg: 'Mínimo 8 caracteres' },
        { test: pass.length <= 20, msg: 'Máximo 20 caracteres' },
        { test: /[A-Z]/.test(pass), msg: 'Al menos una mayúscula' },
        { test: /[a-z]/.test(pass), msg: 'Al menos una minúscula' },
        { test: /\d/.test(pass), msg: 'Al menos un número' },
        { test: /[!@#$%^&*(),.?":{}|<>]/.test(pass), msg: 'Al menos un carácter especial' }
      ];
      return rules.filter(rule => !rule.test).map(rule => `<i class="fas fa-times-circle"></i> ${rule.msg}`);
    }
  };
  
  // Manejo de formularios
  const formHandler = {
    initTooltips: () => {
      document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
      });
    },
  
    setupLogin: () => {
      document.getElementById('loginForm')?.addEventListener('submit', e => {
        e.preventDefault();
        const form = e.target;
        let valid = true;
  
        if (!validators.email(form.username.value) && !validators.username(form.username.value)) {
          form.username.classList.add('is-invalid');
          valid = false;
        } else {
          form.username.classList.remove('is-invalid');
        }
  
        if (form.password.value.length < 8) {
          form.password.classList.add('is-invalid');
          valid = false;
        } else {
          form.password.classList.remove('is-invalid');
        }
  
        if (valid) alert('Inicio de sesión exitoso (simulado)');
      });
    },
  
    setupRegister: () => {
      const form = document.getElementById('createUserForm');
      if (!form) return;
  
      form.addEventListener('submit', e => {
        e.preventDefault();
        let valid = true;
  
        if (!validators.email(form.user.value) && !validators.username(form.user.value)) {
          form.user.classList.add('is-invalid');
          valid = false;
        } else {
          form.user.classList.remove('is-invalid');
        }
  
        const passErrors = validators.password(form.pass.value);
        if (passErrors.length) {
          form.pass.classList.add('is-invalid');
          document.getElementById('passwordError').innerHTML = passErrors.join('<br>');
          valid = false;
        } else {
          form.pass.classList.remove('is-invalid');
        }
  
        if (!form.direccion.value.trim()) {
          form.direccion.classList.add('is-invalid');
          valid = false;
        } else {
          form.direccion.classList.remove('is-invalid');
        }
  
        if (!validators.phone(form.contacto.value)) {
          form.contacto.classList.add('is-invalid');
          valid = false;
        } else {
          form.contacto.classList.remove('is-invalid');
        }
  
        if (valid) alert('Registro exitoso (simulado)');
      });
  
      form.pass.addEventListener('input', e => {
        const errors = validators.password(e.target.value);
        const errorElement = document.getElementById('passwordError');
        errorElement.innerHTML = errors.length ? 
          errors.join('<br>') : 
          '<span class="text-success"><i class="fas fa-check-circle"></i> Contraseña válida</span>';
      });
    },
  
    init: () => {
      formHandler.initTooltips();
      formHandler.setupLogin();
      formHandler.setupRegister();
    }
  };
  
  // Inicializar cuando el DOM esté listo
  document.addEventListener('DOMContentLoaded', formHandler.init);