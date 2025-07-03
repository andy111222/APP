document.addEventListener('DOMContentLoaded', () => {
    const options = document.querySelectorAll('input[type="radio"]');
    const buttons = document.querySelectorAll('button[type="submit"]');
    const form = document.querySelector('form');

    const enableButtonIfSelected = () => {
        const selected = [...options].some(opt => opt.checked);
        buttons.forEach(button => button.disabled = !selected);
    };

    options.forEach(option => {
        option.addEventListener('change', () => {
            enableButtonIfSelected();

            // Optional: highlight selected
            document.querySelectorAll('.option-label').forEach(label => {
                label.classList.remove('selected');
            });
            const label = option.closest('.option-label');
            if (label) label.classList.add('selected');
        });
    });

    enableButtonIfSelected(); // On load
});

