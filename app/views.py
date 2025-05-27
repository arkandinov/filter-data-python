import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

def transaksi_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'app', 'data.json')
    with open(file_path) as f:
        data = json.load(f)

    # Kolom filter yang dipakai (2 kolom)
    filter_columns = ['nama_klien', 'tanggal']

    # Ambil filter dari query params untuk 2 kolom ini
    filters = {}
    for kolom in filter_columns:
        values = request.GET.getlist(kolom)
        if values:
            filters[kolom] = values

    # Filter data berdasarkan filter yang ada
    data_filtered = data
    for kolom, values in filters.items():
        data_filtered = [d for d in data_filtered if d.get(kolom) in values]

    # Buat opsi dropdown cascading per kolom
    opsi_dropdown = {}
    for kolom in filter_columns:
        # Filter data kecuali filter kolom saat ini supaya dropdown cascading
        filters_except_current = {k: v for k, v in filters.items() if k != kolom}
        data_temp = data
        for k, v in filters_except_current.items():
            data_temp = [d for d in data_temp if d.get(k) in v]

        opsi_dropdown[kolom] = sorted(set(d.get(kolom) for d in data_temp if kolom in d))

    # Jika AJAX request, return JSON hasil filter dan opsi dropdown
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'data': data_filtered,
            'opsi_dropdown': opsi_dropdown,
        })

    # Render template dengan context
    context = {
        'data': data_filtered,
        'opsi_dropdown': opsi_dropdown,
        'selected_filters': filters,
    }
    return render(request, 'app/transaksi.html', context)
