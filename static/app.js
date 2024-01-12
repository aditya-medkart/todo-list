function updateStatus(todoId, status) {
    fetch(`/update_status/${todoId}/${status}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update status');
            }
            location.reload();
            return response.text();
        })
}

function deleteTodo(todoId) {
    if (confirm('Are you sure you want to delete this task?')) {
        fetch(`/delete/${todoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete task');
                }
                location.reload();
                return response.text();
            })
            .then(() => {
                const index = getIndexFromId(todoId);
                document.getElementById(`todo-${index}`).remove();
            })
    }
}

function addTodo() {
    const newTodo = document.getElementById('new_todo').value;
    const newDescription = document.getElementById('new_description').value;

    if (newTodo && newDescription) {
        fetch('/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `new_todo=${encodeURIComponent(newTodo)}&new_description=${encodeURIComponent(newDescription)}`,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add new task');
                }
                location.reload();
                return response.text();
            })
    }
    else{
        alert("Please fill the details");
    }
}

