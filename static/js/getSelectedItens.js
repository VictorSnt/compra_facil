document.getElementById('submitButton').addEventListener('click', function(event) {
    event.preventDefault();

    function getSelectedItems(selector) {
        var selectedItems = [];
        document.querySelectorAll(selector + ':checked').forEach(item => {
            selectedItems.push(item.value);
        });
        return selectedItems;
    }

    var loadingModal = document.querySelector('.lds-roller');
    loadingModal.style.display = 'inline-block';
    var selectedSuppliers = getSelectedItems('.fornecedor');
    var selectedGroups = getSelectedItems('.group');
    var selectedFamilies = getSelectedItems('.family');
    var data = {
        "selectedSuppliers": selectedSuppliers,
        "selectedGroups": selectedGroups,
        "selectedFamilies": selectedFamilies
    };
    console.log(data)
    // Converter o objeto em uma string JSON
    var jsonData = JSON.stringify(data);
    console.log(data)
    // Construir a URL com os dados JSON como parte do corpo da solicitação GET
    var url = 'http://192.168.0.28:5000/lista_compras?data=' + encodeURIComponent(jsonData);

    // Enviar solicitação GET
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Ocorreu um erro ao obter os dados.');
        }
        return response.json();
    })
    .then(responseData => {
        loadingModal.style.display = 'none';
        window.location.href = 'http://192.168.0.28:5000/informacoes';
    })
    .catch(error => {
        console.error('Erro:', error);
        // Lidar com o erro, se necessário
    });
});