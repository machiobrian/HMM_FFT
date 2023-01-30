#include <fstream>
#include <vector>
#include <sndfile.h>
#include <iostream>

// define a function that loads a wavfile
std::vector<double> load_audio_sample(const char* file_name)
{
    SF_INFO info; //structure for passing data btn the calling function and the lib when
                  // opening, reading or writing a file
    info.format = 0;
    SNDFILE* file = sf_open(file_name, SFM_READ, &info);

    //load the file -> .wav
    if(!file)
    {
        std::cerr << "Error: Failed to Open the .wav file " << file_name << std::endl;
        return std::vector<double>();
    }

    int num_channels = info.channels;
    int num_samples = info.frames;
    std::vector<double> audio_data(num_samples);

    sf_read_double(file, audio_data.data(), num_samples);
    sf_close(file);

    // if the audio file has multiple channels, average them into a single channel
    if (num_channels > 1)
    {
        std::vector<double> mono_data(num_samples / num_channels);
        for (int i = 0; i < num_samples / num_channels; i++)
        {
            for (int j = 0; j < num_channels; j++)
            {
                mono_data[i] += audio_data[i*num_channels +j];
            }
            mono_data[i] /= num_channels;
        }
        audio_data = mono_data;
    }
    return audio_data;
}

int main(int argc, char** argv)
{
    if(argc < 2)
    {
        std::cerr << "Error: Specify a wave file to load." << std::endl;
        return 1;
    }

    std::vector<double> audio_data = load_audio_sample(argv[1]);
    if(audio_data.empty())
    {
        return 1;
    }


    // mfcc extraction code ...
    return 0;
}