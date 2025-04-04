from pytube import YouTube
from pywebio.input import input, actions
from pywebio.output import put_text, put_success, put_error, put_html, clear
from pywebio import start_server

def download_video():
    put_html("<h1 style='color:blue; text-align:center;'>YouTube Video Downloader</h1>")
    
    while True:
        action = actions(label="O que deseja fazer?", buttons=["Baixar vídeo", "Sair"])

        if action == "Sair":
            put_text("Programa encerrado. Até logo!").style("color: gray; font-size: 20px")
            break

        link_video = input("Insira o link do vídeo do YouTube:")

        if "youtube.com" not in link_video and "youtu.be" not in link_video:
            put_error("Link inválido! Por favor, insira um link do YouTube.")
            continue

        try:
            clear()
            put_html("<h2 style='color:orange;'>Download em andamento...</h2>")

            yt = YouTube(link_video)
            video = yt.streams.get_highest_resolution()

            # Caminho padrão de download
            path_to_download = r'C:\Users\Asus\Downloads'
            video.download(path_to_download)

            put_success(f"✅ Vídeo '{yt.title}' baixado com sucesso!")
            put_text(f"Arquivo salvo em: {path_to_download}")
        
        except Exception as e:
            put_error(f"❌ Ocorreu um erro durante o download: {e}")

# Iniciar servidor web local (acessível no navegador)
if __name__ == "__main__":
    start_server(download_video, port=8080, debug=True)
