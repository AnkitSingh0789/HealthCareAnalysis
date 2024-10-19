document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.symptom-button');
    const selectedSymptomsInput = document.getElementById('selected-symptoms');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('selected');
            updateSelectedSymptoms();
        });
    });

    function updateSelectedSymptoms() {
        const selected = Array.from(buttons)
            .filter(button => button.classList.contains('selected'))
            .map(button => button.value);
        selectedSymptomsInput.value = selected.join(',');
    }
});