new gridjs.Grid({
    columns: [
        { id: 'id', hidden: true },
        { id: 'category_id', hidden: true },
        { id: 'manufacturer_id', hidden: true },
        { id: 'name', name: 'Název', formatter: (_, row) => gridjs.html(`<a href="/sensor/${row.cells[0].data}" class="table-link fw-bold">${row.cells[3].data}</a>`) },
        { id: 'category_name', name: 'Kategorie', formatter: (_, row) => gridjs.html(`<a href="/category/${row.cells[1].data}" class="table-link">${row.cells[4].data}</a>`) },
        { id: 'manufacturer_name', name: 'Výrobce', formatter: (_, row) => gridjs.html(`<a href="/manufacturer/${row.cells[2].data}" class="table-link">${row.cells[5].data}</a>`) },
        //{ id: 'price', name: 'Průměrná cena [Kč]' },
    ],
    pagination: {
        enable: true,
        limit: 10,
    },
    search: true,
    sort: true,
    className: {
        table: 'sensor-table'
    },
    language: {
        'search': {
            'placeholder': 'Zadejte hledaný výraz',
        },
        'sort': {
            'sortAsc': 'Seřadit vzestupně',
            'sortDesc': 'Seřadit sestupně',
        },
        'pagination': {
            'previous': 'Předchozí',
            'next': 'Další',
            'navigate': (page, pages) => `Stránka ${page} z ${pages}`,
            'page': (page) => `Stránka ${page}`,
            'showing': 'Zobrazuji',
            'of': 'z celkových',
            'to': 'až',
            'results': 'výsledků',
        },
        'loading': 'Načítám...',
        'noRecordsFound': 'Nebyly nalezeny žádné odpovídající záznamy',
        'error': 'Došlo k chybě',
    },
    server: {
        url: data_url,
        then: results => results.data.map(sensor => [
            sensor.id,
            sensor.category_id,
            sensor.manufacturer_id,
            sensor.name,
            sensor.category_name,
            sensor.manufacturer_name,
            //sensor.price,
        ]),
    },
}).render(document.getElementById("table-wrapper"));