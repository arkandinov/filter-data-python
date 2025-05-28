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
    filters = {}
    for kolom in filter_columns:
        values = request.GET.getlist(kolom)
        if values:
            filters[kolom] = values

    # Default data kosong kalau tidak ada filter dan bukan AJAX
    data_filtered = []

    # Kalau AJAX dan ada filter atau tombol process data (misal ada param process=1)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if filters:
            data_filtered = data
            for kolom, values in filters.items():
                data_filtered = [d for d in data_filtered if d.get(kolom) in values]
        elif request.GET.get('process') == '1':
            # Load semua data kalau ada param process=1 (tombol Process Data)
            data_filtered = data

        # Opsi dropdown tetap disiapkan untuk filter
        opsi_dropdown = {}
        for kolom in filter_columns:
            filters_except_current = {k: v for k, v in filters.items() if k != kolom}
            data_temp = data
            for k, v in filters_except_current.items():
                data_temp = [d for d in data_temp if d.get(k) in v]
            opsi_dropdown[kolom] = sorted(set(d.get(kolom) for d in data_temp if kolom in d))

        return JsonResponse({
            'data': data_filtered,
            'opsi_dropdown': opsi_dropdown,
        })

    # Render template dengan data kosong saat load page pertama
    context = {
        'data': data_filtered,
        'opsi_dropdown': {},  # bisa kosong atau sesuai kebutuhan
        'selected_filters': filters,
    }
    return render(request, 'app/transaksi.html', context)
