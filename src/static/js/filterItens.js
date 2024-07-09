function filterItems(inputId, listId) {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById(inputId);
    filter = input.value.toUpperCase();
    ul = document.getElementById(listId);
    li = ul.getElementsByClassName('checkbox-item');
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName('label')[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}

// Adicionar eventos de entrada para as barras de pesquisa
document.getElementById('searchInputFornecedor').addEventListener('input', function() {
    filterItems('searchInputFornecedor', 'checkboxListFornecedor');
});
document.getElementById('searchInputGroup').addEventListener('input', function() {
    filterItems('searchInputGroup', 'checkboxListGroup');
});
document.getElementById('searchInputFamily').addEventListener('input', function() {
    filterItems('searchInputFamily', 'checkboxListFamily');
});