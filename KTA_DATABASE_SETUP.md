# Setup Database Monitoring KTA (Google Sheet)

Panduan ini untuk mengaktifkan pencatatan otomatis setiap KTA yang didownload/dicetak ulang ke satu Google Sheet terpusat, supaya admin bisa memonitor tanpa perlu cek satu-satu perangkat mahasiswa.

## Kenapa perlu ini?

Data KTA yang didownload mahasiswa tersimpan di `localStorage` browser mereka masing-masing — itu hanya berguna untuk fitur "Cetak Ulang" di perangkat yang sama, **bukan** untuk admin memantau semua KTA yang pernah terbit. Setup ini menambahkan pencatatan terpusat.

## Langkah Setup (sekali saja, ±10 menit)

### 1. Buat Google Sheet baru
Buka [sheets.new](https://sheets.new), beri nama misalnya "Database KTA Salut Etam Betuah". Di baris 1, isi header kolom persis seperti ini:

```
Timestamp | NIM | Nama | Prodi | Tahun Masuk | Bulan Bukti TF | Tanggal Download | Berlaku Hingga | Cetak Ulang
```

### 2. Buka Apps Script
Di Sheet tadi: menu **Extensions → Apps Script**. Hapus kode default, ganti dengan kode di bawah ini:

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date(),
    data.nim || '',
    data.nama || '',
    data.prodi || '',
    data.tahunMasuk || '',
    data.tfBulan || '',
    data.downloadDate ? new Date(data.downloadDate) : '',
    data.expiryDate ? new Date(data.expiryDate) : '',
    data.isReprint || 'tidak'
  ]);

  return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### 3. Deploy sebagai Web App
- Klik **Deploy → New deployment**
- Pilih tipe **Web app**
- **Execute as:** Me (akun Anda)
- **Who has access:** Anyone
- Klik **Deploy**, izinkan akses saat diminta konfirmasi Google
- Copy URL yang muncul (bentuknya seperti `https://script.google.com/macros/s/AKfycb.../exec`)

### 4. Pasang URL-nya ke kta.html
Buka file `kta.html` di repo, cari baris:

```javascript
var KTA_SHEET_WEBHOOK_URL = '';
```

Ganti jadi:

```javascript
var KTA_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/URL_ANDA/exec';
```

Commit dan push. Selesai — mulai saat itu, setiap KTA yang digenerate atau dicetak ulang otomatis tercatat sebagai baris baru di Sheet.

## Catatan Keamanan

- Sheet ini berisi NIM dan nama mahasiswa — jangan bagikan link Sheet secara publik, cukup akses admin yang perlu.
- Foto mahasiswa **tidak** dikirim ke Sheet ini (hanya data teks), jadi tidak ada isu privasi foto.
- Selama `KTA_SHEET_WEBHOOK_URL` masih kosong, fitur ini otomatis nonaktif dan tidak mengganggu proses download KTA sama sekali — aman untuk di-deploy dulu tanpa setup ini, lalu diaktifkan belakangan.
