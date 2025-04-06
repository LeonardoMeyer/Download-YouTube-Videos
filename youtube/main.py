from pytube import YouTube
from pywebio.input import input, actions, select
from pywebio.output import put_text, put_success, put_error, put_html, clear
from pywebio import start_server

def download_video():
    # Idioma / Language / Sprache
    lang = select("Choose your language / Escolha o idioma / Sprache wählen:", 
                  options=["English", "Português", "Deutsch"])

    def t(en, pt, de):
        return {"English": en, "Português": pt, "Deutsch": de}[lang]

    put_html(f"<h1 style='color:blue; text-align:center;'>YouTube {t('Video Downloader', 'Video Downloader', 'Video-Downloader')}</h1>")

    while True:
        action = actions(label=t("What would you like to do?", "O que deseja fazer?", "Was möchten Sie tun?"),
                         buttons=[t("Download Video", "Baixar vídeo", "Video herunterladen"),
                                  t("Exit", "Sair", "Beenden")])

        if action == t("Exit", "Sair", "Beenden"):
            put_text(t("Program terminated. See you next time!",
                       "Programa encerrado. Até logo!",
                       "Programm beendet. Bis zum nächsten Mal!")).style("color: gray; font-size: 20px")
            break

        video_link = input(t("Enter the YouTube video link:",
                             "Insira o link do vídeo do YouTube:",
                             "Fügen Sie den YouTube-Link ein:"))

        if "youtube.com" not in video_link and "youtu.be" not in video_link:
            put_error(t("Invalid link! Please enter a valid YouTube link.",
                        "Link inválido! Por favor, insira um link do YouTube.",
                        "Ungültiger Link! Bitte fügen Sie einen gültigen YouTube-Link ein."))
            continue

        try:
            clear()
            put_html(f"<h2 style='color:orange;'>{t('Downloading...', 'Baixando...', 'Wird heruntergeladen...')}</h2>")

            yt = YouTube(video_link)
            video = yt.streams.get_highest_resolution()  # ✅ mais compatível e direto

            path_to_download = r'C:\Users\Propulsor404\Downloads'
            video.download(path_to_download)

            put_success(f"✅ {t('Video', 'Vídeo', 'Video')} '{yt.title}' {t('downloaded successfully!', 'baixado com sucesso!', 'erfolgreich heruntergeladen!')}")
            put_text(f"{t('File saved to', 'Arquivo salvo em', 'Datei gespeichert in')}: {path_to_download}")

        except Exception as e:
            put_error(f"❌ {t('An error occurred during download', 'Ocorreu um erro durante o download', 'Fehler beim Herunterladen')}: {e}")

if __name__ == "__main__":
    start_server(download_video, port=8080, debug=True)
