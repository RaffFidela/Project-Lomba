from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from ..db import get_db

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/laporan', methods=['GET'])
def get_laporan():
    try:
        conn = get_db()
        rows = conn.execute('SELECT * FROM laporan ORDER BY id DESC').fetchall()
        
        data = []
        for row in rows:
            data.append({
                'id': row['id'],
                'nama': row['nama'],
                'kelas': row['kelas'],
                'lokasi': row['lokasi'],
                'deskripsi': row['deskripsi'],
                'status': row['status'],
                'waktu_lapor': row['waktu_lapor'],
                'waktu_selesai': row['waktu_selesai'],
                'foto1': row['foto1'],
                'foto2': row['foto2'],
                'foto3': row['foto3']
            })
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"Error getting laporan: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/laporan', methods=['POST'])
def tambah_laporan():
    try:
        nama = request.form.get('nama', '').strip()
        kelas = request.form.get('kelas', '').strip()
        lokasi = request.form.get('lokasi', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()

        if not all([nama, kelas, lokasi, deskripsi]):
            return jsonify({'error': 'Semua field wajib diisi'}), 400

        foto_files = []
        for i in range(1, 4):
            file = request.files.get(f'foto{i}')
            if not file or file.filename == '':
                return jsonify({'error': 'Wajib upload tepat 3 foto'}), 400
            if not allowed_file(file.filename):
                return jsonify({'error': 'Format foto tidak didukung'}), 400
            foto_files.append(file)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        foto_names = []
        for idx, file in enumerate(foto_files, 1):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{timestamp}_{idx}.{ext}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            foto_names.append(filename)

        waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db()
        conn.execute('''
            INSERT INTO laporan (nama, kelas, lokasi, deskripsi, status, waktu_lapor, foto1, foto2, foto3)
            VALUES (?, ?, ?, ?, 'Menunggu', ?, ?, ?, ?)
        ''', (nama, kelas, lokasi, deskripsi, waktu_sekarang, foto_names[0], foto_names[1], foto_names[2]))
        conn.commit()

        return jsonify({'message': 'Laporan berhasil dikirim'}), 201
    except Exception as e:
        current_app.logger.error(f"Error adding laporan: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/laporan/<int:id>/status', methods=['PUT'])
def update_status(id):
    try:
        data = request.get_json()
        if not data:
             return jsonify({'error': 'Data JSON tidak ditemukan'}), 400
        
        status_baru = data.get('status')
        if status_baru not in ['Dikerjakan', 'Selesai']:
            return jsonify({'error': 'Status tidak valid'}), 400

        conn = get_db()
        if status_baru == 'Selesai':
            waktu_selesai = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute('UPDATE laporan SET status = ?, waktu_selesai = ? WHERE id = ?',
                         (status_baru, waktu_selesai, id))
        else:
            conn.execute('UPDATE laporan SET status = ? WHERE id = ?', (status_baru, id))

        conn.commit()
        return jsonify({'message': 'Status berhasil diubah'})
    except Exception as e:
        current_app.logger.error(f"Error updating status for {id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
