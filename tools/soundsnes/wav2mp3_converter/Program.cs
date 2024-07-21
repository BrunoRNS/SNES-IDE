using System;
using System.IO;
using System.Windows.Forms;
using NAudio.Wave;
using NAudio.Lame;

namespace wav2mp3_converter
{
    internal static class Program
    {

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Wave files|*.wav"
            };

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string inputFilePath = openFileDialog.FileName;
                string outputFilePath = Path.ChangeExtension(inputFilePath, ".mp3");

                try
                {
                    
                    using (var reader = new WaveFileReader(inputFilePath))
                    {
                        using (var writer = new LameMP3FileWriter(outputFilePath, reader.WaveFormat, 64))
                        {
                            reader.CopyTo(writer);
                        }
                    }

                    ShowMessage("Success", $"Mp3 file in: {outputFilePath}");
                }
                catch (Exception ex)
                {
                    ShowMessage("Error!",$"Error while converting: {ex.Message}");
                }

            }
        }
        static void ShowMessage(string title, string message)
        {
            MessageBox.Show(message, title, MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
