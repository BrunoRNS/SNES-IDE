from pathlib import Path
import ctypes

class Typing:

    def __init__(self):

        self.lame_dll = ctypes.CDLL('lame_enc.dll')
        self.sdl_dll = ctypes.CDLL('SDL2.dll')

        self.lame_init = self.lame_dll.lame_init
        self.lame_set_num_channels = self.lame_dll.lame_set_num_channels
        self.lame_set_sample_rate = self.lame_dll.lame_set_sample_rate
        self.lame_set_bit_rate = self.lame_dll.lame_set_bit_rate
        self.lame_encode_buffer = self.lame_dll.lame_encode_buffer
        self.lame_close = self.lame_dll.lame_close

        self.sdl_init = self.sdl_dll.SDL_Init
        self.sdl_quit = self.sdl_dll.SDL_Quit


class LameEncoder:

    def __init__(self, typing):

        self.typing = typing
        self.lame = self.typing.lame_init()

    def set_num_channels(self, channels):

        self.typing.lame_set_num_channels(self.lame, channels)

    def set_sample_rate(self, sample_rate):

        self.typing.lame_set_sample_rate(self.lame, sample_rate)

    def set_bit_rate(self, bit_rate):

        self.typing.lame_set_bit_rate(self.lame, bit_rate)

    def encode_buffer(self, buffer, buffer_size):

        mp3_buffer = ctypes.create_string_buffer(buffer_size * 2)
        self.typing.lame_encode_buffer(self.lame, buffer, buffer_size, mp3_buffer, buffer_size * 2)

        return mp3_buffer.raw

    def close(self):

        self.typing.lame_close(self.lame)

class SdlInitializer:

    def __init__(self, typing):

        self.typing = typing
        self.typing.sdl_init(0x00000010)

    def quit(self):

        self.typing.sdl_quit()

class WavToMp3Converter:

    def __init__(self, input_file, output_file):

        self.input_file = input_file
        self.output_file = output_file

        self.typing = Typing()

        self.lame_encoder = LameEncoder(self.typing)
        self.sdl_initializer = SdlInitializer(self.typing)

    def convert(self):

        try:

            with open(self.input_file, 'rb') as wav_file:

                header = wav_file.read(44)

                if header[:4] != b'RIFF' or header[8:12] != b'WAVE':

                    print('Error: file is not a WAV')
                    return

                sample_rate = int.from_bytes(header[24:28], byteorder='little')
                bits_per_sample = int.from_bytes(header[34:36], byteorder='little')
                channels = int.from_bytes(header[22:24], byteorder='little')

                self.lame_encoder.set_num_channels(channels)
                self.lame_encoder.set_sample_rate(sample_rate)
                self.lame_encoder.set_bit_rate(128)

                with open(self.output_file, 'wb') as mp3_file:

                    buffer_size = 1024

                    while True:

                        buffer = wav_file.read(buffer_size)

                        if not buffer:

                            break

                        mp3_buffer = self.lame_encoder.encode_buffer(buffer, len(buffer))
                        mp3_file.write(mp3_buffer)

            self.lame_encoder.close()

            self.sdl_initializer.quit()


        except Exception as e:

            print(f"An error occurred: {e}")



def main():

    print("\nUsage: <input_file_path.wav> <output_file_path.mp3>\n")

    entry: list[str] = input().strip().split(" ")

    if len(entry) != 2:

        print("Got too many arguments or to less arguments, expected 2")

        main()

    elif (not Path(entry[0]).exists()) or (not Path(entry[1]).parent.exists()):

        print("Input file or output path does not exist")

        main()
    
    elif not ((Path(entry[0]).is_file()) or (Path(entry[1]).is_file())):

        print("Input or Output file is not a file.")

        main()

    elif not (entry[0].endswith(".wav") or entry[1].endswith(".mp3")):

        print("Expected wav and mp3 files, got unknown")

        main()

    converter = WavToMp3Converter(*entry)
    converter.convert()
