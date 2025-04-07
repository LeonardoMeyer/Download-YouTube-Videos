import tkinter as tk
from tkinter import filedialog

from pytube import YouTube
from pywebio.input import input, actions, select
from pywebio.output import (
    put_text, put_success, put_error, put_html,
    clear, put_processbar, set_processbar
)
from pywebio import start_server


def download_video():
    # Escolher idioma
    lang = select("Choose your language / Escolha o idioma / Sprache wählen:",
                  options=["English", "Português", "Deutsch"])

    def t(en, pt, de):
        return {"English": en, "Português": pt, "Deutsch": de}[lang]

    put_html(f"<h1 style='color:blue; text-align:center;'>YouTube {t('Video Downloader', 'Baixador de Vídeo', 'Video-Downloader')}</h1>")

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
            yt = YouTube(video_link)

            # Mostrar opções de resolução
            streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
            resolutions = list({stream.resolution for stream in streams if stream.resolution})
            chosen_res = select(t("Choose resolution", "Escolha a resolução", "Wählen Sie die Auflösung:"), resolutions)
            video = yt.streams.filter(res=chosen_res, progressive=True).first()

            # Abrir janela para selecionar local de salvamento
            root = tk.Tk()
            root.withdraw()
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")],
                title=t("Choose file save location", "Escolha onde salvar o arquivo", "Speicherort auswählen")
            )

            if not save_path:
                put_error(t("No location selected!", "Nenhum local selecionado!", "Kein Speicherort ausgewählt!"))
                continue

            put_html(f"<h3 style='color:orange;'>{t('Downloading...', 'Baixando...', 'Herunterladen...')}</h3>")
            put_processbar("bar")

            def progress_callback(stream, chunk, bytes_remaining):
                total = stream.filesize
                percent = (total - bytes_remaining) / total
                set_processbar("bar", percent)

            yt.register_on_progress_callback(progress_callback)

            video.download(filename=save_path)
            put_success(f"✅ {t('Video', 'Vídeo', 'Video')} '{yt.title}' {t('downloaded successfully!', 'baixado com sucesso!', 'erfolgreich heruntergeladen!')}")
            put_text(f"{t('Saved to', 'Salvo em', 'Gespeichert in')}: {save_path}")

        except Exception as e:
            put_error(f"❌ {t('An error occurred during download', 'Ocorreu um erro durante o download', 'Fehler beim Herunterladen')}: {e}")


if __name__ == "__main__":
    start_server(download_video, port=8080, debug=True)
