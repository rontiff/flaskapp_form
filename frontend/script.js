document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const contactList = document.getElementById('contactList');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            firstName: formData.get('firstName'),
            lastName: formData.get('lastName'),
            email: formData.get('email'),
            number: formData.get('number'),
        };

        fetch('http://127.0.0.1:5000/create_contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(json => {
            if (json.message === "User created") {
                messageDiv.textContent = "Contact added successfully!";
                messageDiv.style.color = 'green';
                form.reset();
                loadContacts();
            } else {
                messageDiv.textContent = json.message;
                messageDiv.style.color = 'red';
            }
        })
        .catch(error => {
            messageDiv.textContent = "An error occurred!";
            messageDiv.style.color = 'red';
        });
    });

    function loadContacts() {
        fetch('http://127.0.0.1:5000/contacts')
        .then(response => response.json())
        .then(json => {
            // Clear existing content
            contactList.innerHTML = '';
    
            // Create the table and header row
            const table = document.createElement('table');
            table.classList.add('contact-table');
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
                <th>Number</th>
                <th>Actions</th>
            `;
            thead.appendChild(headerRow);
            table.appendChild(thead);
    
            // Create the table body and populate it with data
            const tbody = document.createElement('tbody');
            json.contacts.forEach(contact => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${contact.firstName}</td>
                    <td>${contact.lastName}</td>
                    <td>${contact.email}</td>
                    <td>${contact.number}</td>
                    <td>
                        <button class="update-button" onclick="updateContact(${contact.id})">Update</button>
                        <button class="delete-button" onclick="deleteContact(${contact.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
    
            // Append the table to the contact list container
            contactList.appendChild(table);
        })
        .catch(error => {
            contactList.innerHTML = 'Failed to load contacts';
        });
    }

    window.deleteContact = function(id) {
        fetch(`http://127.0.0.1:5000/update_contact/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(json => {
            messageDiv.textContent = json.message;
            messageDiv.style.color = json.message === "User deleted" ? 'green' : 'red';
            loadContacts();
        })
        .catch(error => {
            messageDiv.textContent = "An error occurred!";
            messageDiv.style.color = 'red';
        });
    };

    window.updateContact = function(id) {
        const newFirstName = prompt("Enter new first name:");
        const newLastName = prompt("Enter new last name:");
        const newEmail = prompt("Enter new email:");
        const newNumber = prompt("Enter new number:");

        if (newFirstName && newLastName && newEmail) {
            const data = {
                firstName: newFirstName,
                lastName: newLastName,
                email: newEmail,
                number: newNumber,
            };

            fetch(`http://127.0.0.1:5000/update_contact/${id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(json => {
                messageDiv.textContent = json.message;
                messageDiv.style.color = json.message === "User updated" ? 'green' : 'red';
                loadContacts();
            })
            .catch(error => {
                messageDiv.textContent = "An error occurred!";
                messageDiv.style.color = 'red';
            });
        }
    };

    loadContacts();
});
