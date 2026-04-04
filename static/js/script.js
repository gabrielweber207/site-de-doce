// JS Functions for Store

// Auto-close flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.alert');
    if(flashMessages) {
        flashMessages.forEach(msg => {
            setTimeout(() => {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-10px)';
                setTimeout(() => msg.remove(), 300);
            }, 4000);
            
            // Manual close
            const closeBtn = msg.querySelector('.close-btn');
            if(closeBtn) {
                closeBtn.addEventListener('click', () => {
                    msg.style.opacity = '0';
                    setTimeout(() => msg.remove(), 300);
                });
            }
        });
    }

    // Mobile Navbar Toggle
    const mobileBtn = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    if(mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Dropdown toggle mobile support
    const dropBtn = document.querySelector('.dropdown-btn');
    if(dropBtn) {
        dropBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const content = dropBtn.nextElementSibling;
            content.classList.toggle('active');
        });
    }
});

// Carrinho de Compras - Increment/Decrement handlers
function incrementar(btn) {
    const input = btn.previousElementSibling;
    input.value = parseInt(input.value) + 1;
    input.dispatchEvent(new Event('change'));
}

function decrementar(btn) {
    const input = btn.nextElementSibling;
    if (parseInt(input.value) > 0) {
        input.value = parseInt(input.value) - 1;
        input.dispatchEvent(new Event('change'));
    }
}
