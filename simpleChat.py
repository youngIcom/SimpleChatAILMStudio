import requests
import os
from colorama import init, Fore, Style
import subprocess

# Inisialisasi colorama
init()

# Konfigurasi
API_URL = "http://192.168.2.167:1234/v1/chat/completions"

# Konfigurasi Coqui TTS
MODEL_FILE_PATH = "checkpoint_1260000-inference.pth"
CONFIG_FILE_PATH = "config.json"
SPEAKERS_FILE_PATH = "speakers.pth"  # Tambahkan path speakers.pth Anda di sini
OUTPUT_WAV = "output_ai.wav"
SPEAKER_IDX = "wibowo"  # Ganti sesuai speaker yang tersedia di model Anda

def synthesize_speech_coqui(text_to_speak, model_path, config_path, output_path, speaker_idx=None, speakers_file=None):
    """
    Mensintesis ucapan menggunakan Coqui TTS melalui command-line interface.
    """
    if not os.path.exists(model_path):
        return False, f"Error: File model tidak ditemukan di {model_path}"
    if not os.path.exists(config_path):
        return False, f"Error: File konfigurasi tidak ditemukan di {config_path}"
    if speakers_file and not os.path.exists(speakers_file):
        return False, f"Error: File speakers tidak ditemukan di {speakers_file}"

    command = [
        "tts",
        "--text", text_to_speak,
        "--model_path", model_path,
        "--config_path", config_path,
        "--out_path", output_path
    ]
    if speaker_idx:
        command.extend(["--speaker_idx", speaker_idx])
    if speakers_file:
        command.extend(["--speakers_file", speakers_file])

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=60)
        if process.returncode == 0 and os.path.exists(output_path):
            print(f"Sintesis berhasil! Audio disimpan di: {output_path}")
            return True, stdout
        else:
            print(f"Sintesis gagal. Return code: {process.returncode}")
            print(f"Stdout: {stdout}")
            print(f"Stderr: {stderr}")
            if not os.path.exists(output_path):
                print(f"File output {output_path} tidak ditemukan setelah sintesis.")
            return False, stderr
    except FileNotFoundError:
        error_msg = "Error: Perintah 'tts' tidak ditemukan. Pastikan Coqui TTS sudah terinstal dan ada di PATH sistem Anda."
        print(error_msg)
        return False, error_msg
    except subprocess.TimeoutExpired:
        error_msg = "Error: Proses sintesis melebihi batas waktu."
        print(error_msg)
        process.kill()
        stdout, stderr = process.communicate()
        return False, error_msg + f"\nStdout: {stdout}\nStderr: {stderr}"
    except Exception as e:
        error_msg = f"Terjadi kesalahan saat menjalankan perintah tts: {e}"
        print(error_msg)
        return False, error_msg

def chat_with_ai():
    print(f"{Fore.GREEN}\n=== Local AI Chat ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Ketik 'exit' untuk keluar{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Terhubung ke: {API_URL}{Style.RESET_ALL}\n")
    
    chat_history = []
    while True:
        try:
            user_input = input(f"{Fore.BLUE}Anda: {Style.RESET_ALL}").strip()
            if user_input.lower() in ['exit', 'quit', 'keluar']:
                print(f"{Fore.GREEN}Sampai jumpa!{Style.RESET_ALL}")
                break
            if not user_input:
                continue

            chat_history.append({"role": "user", "content": user_input})
            data = {
                "model": "llama3-8b-cpt-sahabatai-v1-instruct",  # Ganti sesuai model server Anda
                "messages": chat_history,
                "temperature": 0.7,
                "max_tokens": 80
            }
            print(f"{Fore.YELLOW}AI sedang memproses...{Style.RESET_ALL}", end='\r')

            response = requests.post(API_URL, json=data)

            if response.status_code == 200:
                ai_response = response.json()["choices"][0]["message"]["content"]
                chat_history.append({"role": "assistant", "content": ai_response})
                print(f"{Fore.GREEN}AI: {Style.RESET_ALL}{ai_response}\n")
                subprocess.run('espeak-ng', shell=True, check=True, input=ai_response.encode('utf-8'))

                
            # untuk menjalankan Coqui TTS, uncomment bagian berikut:
            #Coqui TTS
            #     success, msg = synthesize_speech_coqui(
            #         ai_response,
            #         MODEL_FILE_PATH,
            #         CONFIG_FILE_PATH,
            #         OUTPUT_WAV,
            #         speaker_idx=SPEAKER_IDX,
            #         speakers_file=SPEAKERS_FILE_PATH
            #     )
            #     if success:
            #         if os.path.exists(OUTPUT_WAV):
            #             play_status = os.system(f'aplay {OUTPUT_WAV}')
            #             if play_status != 0:
            #                 print(f"{Fore.RED}Error saat memutar audio dengan aplay. Pastikan aplay terinstal dan file {OUTPUT_WAV} valid.{Style.RESET_ALL}")
            #             else:
            #                 print(f"{Fore.GREEN}Audio berhasil diputar.{Style.RESET_ALL}")
            #         else:
            #             print(f"{Fore.RED}File {OUTPUT_WAV} tidak ditemukan untuk diputar.{Style.RESET_ALL}")
            #     else:
            #         print(f"{Fore.RED}Model mengalami masalah ketika memutar: {msg}{Style.RESET_ALL}")
            # else:
            #     print(f"\n{Fore.RED}Error: {response.status_code} - {response.text}{Style.RESET_ALL}\n")
        except requests.exceptions.ConnectionError:
            print(f"\n{Fore.RED}Gagal terhubung ke server. Pastikan LM Studio/AI server sedang berjalan.{Style.RESET_ALL}")
            break
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Dihentikan oleh pengguna{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    chat_with_ai()