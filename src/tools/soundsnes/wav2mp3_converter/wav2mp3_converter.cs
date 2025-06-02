using System;
using System.IO;
using NAudio.Wave;
using NAudio.Lame;

namespace wav2mp3_converter
{
    /// <summary>
    /// CLI-only WAV to MP3 converter.
    /// </summary>
    internal static class Program {

        static void Main(string[] args) {

            Console.WriteLine("WAV to MP3 Converter (CLI)");
            Console.Write("Enter the full path to the input WAV file: ");
            string inputFilePath = Console.ReadLine()?.Trim();

            if (string.IsNullOrEmpty(inputFilePath) || !File.Exists(inputFilePath)) {

                Console.WriteLine("Error: File not found or invalid input.");
                return;

            }

            string defaultOutput = Path.ChangeExtension(inputFilePath, ".mp3");
            Console.Write($"Enter output MP3 file path [default: {defaultOutput}]: ");
            string outputFilePath = Console.ReadLine()?.Trim();

            if (string.IsNullOrEmpty(outputFilePath)) {

                outputFilePath = defaultOutput;
            }

            try {

                ConvertWavToMp3(inputFilePath, outputFilePath);
                Console.WriteLine($"Success! MP3 file created at: {outputFilePath}");

            } catch (Exception ex) {

                Console.WriteLine($"Error while converting: {ex.Message}");

            }

        }

        static void ConvertWavToMp3(string inputFilePath, string outputFilePath) {

            using (var reader = new WaveFileReader(inputFilePath))
            using (var writer = new LameMP3FileWriter(outputFilePath, reader.WaveFormat, 64)) {

                reader.CopyTo(writer);

            }
        }
    }
}