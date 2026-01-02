document.addEventListener('DOMContentLoaded', () => {
    // Mobile Sidebar Toggle (implementation pending HTML trigger)
    console.log('Admin Script Loaded');

    // Auto dissmiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });
});
