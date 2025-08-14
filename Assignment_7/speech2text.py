from transformers import VitsModel, AutoTokenizer
import torch
import scipy

# Load the pre-trained Vietnamese TTS model and tokenizer from Hugging Face
model = VitsModel.from_pretrained("facebook/mms-tts-vie")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")

# Define the input text you want to convert to speech
text = "Chào mừng bạn đến với thế giới của công nghệ âm thanh. Hãy cùng khám phá những điều thú vị nhé!"

# Tokenize the input text and prepare it for the model
inputs = tokenizer(text, return_tensors="pt")

# Run the model to generate waveform output, disabling gradient calculation for efficiency
with torch.no_grad():
    output = model(**inputs).waveform  # Forward pass, output is a tensor

# Move the waveform tensor to CPU, convert to numpy array, and remove extra dimensions
output_np = output.cpu().numpy().squeeze()

# Write the waveform data to a .wav audio file using the model's sampling rate
scipy.io.wavfile.write("example.wav", rate=model.config.sampling_rate, data=output_np)
