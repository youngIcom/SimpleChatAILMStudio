# 🤖 Chat AI Lokal dengan Suara (TTS)

Selamat datang di **Chat AI Lokal**!  
Skrip Python sederhana ini memungkinkan kamu mengobrol dengan model AI langsung di komputermu sendiri. Tidak hanya membalas lewat teks, asisten AI ini juga bisa "berbicara" menggunakan Text-to-Speech (TTS).

---

## ✨ Fitur Unggulan

- 💻 **100% Lokal & Privat:** Semua proses chat dan suara berjalan di mesin kamu. Aman, tanpa sensor.
- 🗣️ **Output Suara Fleksibel:**
  - **eSpeak-NG (Default):** Cepat, ringan, dan hemat sumber daya.
  - **Coqui TTS (Opsional):** Suara lebih natural (butuh setup tambahan).
- 🧠 **Kontekstual:** AI mengingat riwayat percakapan dalam satu sesi.
- 🎨 **Tampilan Berwarna:** Terminal lebih hidup berkat `colorama`.
- 🔌 **Mudah Dikonfigurasi:** Ubah beberapa variabel saja untuk menyesuaikan server AI dan model.
- 🛠️ **Penanganan Error:** Pesan jelas jika gagal terhubung ke server AI atau ada masalah lain.

---

## 🔧 Prasyarat

Pastikan semua kebutuhan berikut sudah terpasang di sistem kamu:

- **Python 3.7+**
- **Server AI Lokal:**  
  Contoh: LM Studio, Ollama, dll.  
  > **Pastikan sudah mengunduh model AI (misal: Llama 3, Mistral, dsb) dan menjalankan API Server.**
- **Dependensi Sistem (untuk TTS):**
  - **Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get update && sudo apt-get install espeak-ng aplay
    ```
  - **Windows/MacOS:**  
    Instal eSpeak-NG secara manual.

---

## 🚀 Instalasi & Konfigurasi

1. **Clone Repositori**
    ```bash
    git clone https://github.com/username-kamu/nama-repositori-kamu.git
    cd nama-repositori-kamu
    ```

2. **Buat `requirements.txt`**
    ```
    requests
    colorama
    ```

3. **Buat Virtual Environment (Opsional tapi direkomendasikan)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

4. **Install Library Python**
    ```bash
    pip install -r requirements.txt
    ```

5. **Konfigurasi Skrip Utama**
    - Buka file Python utama.
    - Ubah variabel berikut sesuai kebutuhan:
      ```python
      API_URL = "http://127.0.0.1:1234/v1/chat/completions"  # Ganti jika perlu
      # ...
      data = {
          "model": "nama-model-yang-kamu-pakai",  # Sesuaikan dengan model di server AI
          # ...
      }
      ```

---

## ▶️ Cara Menjalankan

Setelah konfigurasi selesai, jalankan perintah berikut di terminal:

```bash
python nama_file_kamu.py
```

Kamu bisa mulai mengobrol dengan AI lokalmu!  
Ketik `exit` atau `keluar` untuk mengakhiri sesi.

---

## 🔊 (Opsional) Suara Natural dengan Coqui TTS

Ingin suara AI yang lebih natural?  
Ikuti langkah berikut (butuh RAM/VRAM lebih besar):

1. **Install Coqui TTS**
    ```bash
    pip install TTS
    ```

2. **Unduh Model Suara**  
   (dari Hugging Face, dsb. Biasanya terdiri dari `checkpoint.pth`, `config.json`, dan `speakers.pth` jika multi-speaker)

3. **Konfigurasi Skrip**
    - Letakkan file model di folder skrip.
    - Ubah path di skrip:
      ```python
      MODEL_FILE_PATH = "checkpoint_1260000-inference.pth"
      CONFIG_FILE_PATH = "config.json"
      SPEAKERS_FILE_PATH = "speakers.pth"  # Jika ada
      SPEAKER_IDX = "wibowo"  # Sesuaikan dengan speaker yang tersedia
      ```
    - Aktifkan kode Coqui TTS di dalam loop `chat_with_ai`:
      ```python
      # Komentar baris espeak-ng
      # subprocess.run('espeak-ng', ...)

      # Aktifkan blok Coqui TTS
      success, msg = synthesize_speech_coqui(
          ai_response,
          MODEL_FILE_PATH,
          CONFIG_FILE_PATH,
          OUTPUT_WAV,
          speaker_idx=SPEAKER_IDX,
          speakers_file=SPEAKERS_FILE_PATH
      )
      if success:
          if os.path.exists(OUTPUT_WAV):
              play_status = os.system(f'aplay {OUTPUT_WAV}')
              if play_status != 0:
                  print(f"{Fore.RED}Error saat memutar audio...{Style.RESET_ALL}")
      ```

4. **Jalankan kembali skrip**  
   Jika konfigurasi benar, AI akan berbicara dengan suara lebih alami!

---

## 🤔 Troubleshooting

<details>
<summary><strong>Error: <code>requests.exceptions.ConnectionError</code></strong></summary>

**Penyebab:** Skrip tidak bisa terhubung ke server AI.  
**Solusi:**
- Pastikan aplikasi server AI (LM Studio, dll.) sedang berjalan.
- Pastikan sudah menekan tombol "Start Server".
- Periksa kembali `API_URL` di skrip.
- Cek firewall yang mungkin memblokir koneksi lokal.
</details>

<details>
<summary><strong>Error: Perintah 'tts' tidak ditemukan (Coqui)</strong></summary>

**Penyebab:** Library Coqui TTS belum terinstal atau PATH tidak ditemukan.  
**Solusi:**  
Pastikan berada di virtual environment yang benar, lalu jalankan:
```bash
pip install TTS
```
</details>

<details>
<summary><strong>Suara tidak berbunyi di Linux</strong></summary>

**Penyebab:** `aplay` belum terinstal.  
**Solusi:**
```bash
sudo apt-get install alsa-utils
```
</details>

---