document.getElementById('maintenanceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Gather form data
    const studentId = document.getElementById('student_id').value;
    const building = document.getElementById('building').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('tiny').value;

    // Send data to the server
    const formData = {
        student_id: studentId,
        building: building,
        category: category,
        description: description
    };

    fetch('http://127.0.0.1:8080/save-csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            alert('Data saved successfully!');
        } else {
            alert('Error saving data.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
