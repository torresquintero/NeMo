import soundfile as sf
import numpy as np
import argparse

from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="The text to synthesise.", required=True)
    args = parser.parse_args()

    tts_model = FastPitchModel.from_pretrained("tts_en_fastpitch")
    parsed = tts_model.parse(args.text)
    spectrogram = tts_model.generate_spectrogram(tokens=parsed)

    vocoder = HifiGanModel.from_pretrained(model_name="tts_en_hifigan")
    audio = vocoder.convert_spectrogram_to_audio(spec=spectrogram)
    new_audio = audio.to('cpu').detach().numpy()
    
    sf.write("speech.wav", np.ravel(new_audio), 22050)