# Install the requests package by executing the command "pip install requests"

import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "4e2041a7450b469f8af8d58207935971"
}
filename = "./uploads/03704314909/b7a0e4f6-d954-4951-85b0-d4db36c0ab1c.wav"
# You can upload a local file using the following code
with open(filename, "rb") as f:
    response = requests.post(base_url + "/v2/upload",
                         headers=headers,
                         data=f)

audio_url = response.json()["upload_url"]

#audio_url = "https://assembly.ai/wildfires.mp3"


data = {
    "audio_url": audio_url,
    "speech_model": "universal",
    "language_code": "ur",

}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']
polling_endpoint = base_url + "/v2/transcript/" + transcript_id

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()
  transcript_text = transcription_result['text']

  if transcription_result['status'] == 'completed':
    print(f"Transcript Text:", transcript_text)
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)