function toggleAllSupplier(checked) {
    document.querySelectorAll('.fornecedor').forEach(item => {
        item.checked = checked;
    });
}

document.getElementById('selectAllFornecedor').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllSupplier(true);
});

document.getElementById('deselectAllFornecedor').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllSupplier(false);
});

function toggleAllGroups(checked) {
    document.querySelectorAll('.group').forEach(item => {
        item.checked = checked;
    });
}

document.getElementById('selectAllGroup').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllGroups(true);
});

document.getElementById('deselectAllGroup').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllGroups(false);
});

function toggleAllFamilies(checked) {
    document.querySelectorAll('.family').forEach(item => {
        item.checked = checked;
    });
}

document.getElementById('selectAllFamily').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllFamilies(true);
});

document.getElementById('deselectAllFamily').addEventListener('click', function(event) {
    event.preventDefault();
    toggleAllFamilies(false);
});