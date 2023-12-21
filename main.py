import os
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import  BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pytube import YouTube
from pytube.exceptions import RegexMatchError, AgeRestrictedError

# link = "https://www.youtube.com/watch?v=Uw_hZfH5Ukc"
video_format = ""
quality = ""


class MyLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        # Bind the update_layout method to Window size changes
        Window.bind(on_resize=self.update_layout)

        # Call update_layout initially to set the initial sizes
        self.update_layout()

    def update_layout(self, *args):
        # Get the screen size
        screen_width, screen_height = Window.size

        # Set the size of the Image widget
        image_widget = self.ids.image_widget
        image_widget.size_hint = (0.8, 0.8)
        image_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Set the size of the Label and TextInput widgets
        label_widget1 = self.ids.label_widget1
        label_widget1.font_size = int(screen_width / 20)
        label_widget2 = self.ids.label_widget2
        label_widget2.font_size = int(screen_width / 20)
        label_widget3 = self.ids.label_widget3
        label_widget3.font_size = int(screen_width / 20)
        label_widget4 = self.ids.label_widget4
        label_widget4.font_size = int(screen_width / 20)

        text_input_widget = self.ids.text_input
        text_input_widget.width = int(screen_width / 1.36)
        text_input_widget.font_size = int(screen_width / 21)


    def spinner_clicked(self, value):
        global video_format
        video_format = value

    def spinner_quality(self, value):
        global quality
        quality = value

    def show_popup(self, title, content):
        def open_popup(dt):
            popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
            popup.open()

        Clock.schedule_once(open_popup, 0)

    def download_thread(self, link):
        try:
            yt = YouTube(link)
        except RegexMatchError:
            self.show_popup("Invalid Link", "pLease enter a valid link.")
        else:
            if video_format == "Mp3":
                mp4files = yt.streams.filter(only_audio=True, file_extension="mp4").first()
                audio_file_path = mp4files.download(f"{yt.title}mp3")

                mp3_file_path = audio_file_path.replace(".mp4", ".mp3")
                os.rename(audio_file_path, mp3_file_path)
            elif video_format == "Mp4":
                if quality:
                    try:
                        mp4files = yt.streams.filter(file_extension="mp4")
                    except AgeRestrictedError:
                        self.show_popup("Age Restricted", "You are trying to download age restricted content")
                    else:
                        mp4files.get_by_resolution(quality).download()

            else:
                self.show_popup("Video Format error", "Choose correct format.")

    def video_downloader(self):
        text_input = self.ids.text_input
        link = text_input.text
        if link:
            thread = threading.Thread(target=self.download_thread, args=(link,))
            thread.start()
        else:
            self.show_popup("Empty Filed", "Please enter a link to download.")


class YoutubeDownloaderApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    YoutubeDownloaderApp().run()



