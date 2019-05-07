import os
import time
import xml.etree.ElementTree as ET

from pydub import AudioSegment
import requests
import youtube_dl

VIDEO_URLS = ['https://www.youtube.com/watch?v=8ZZ6GrzWkw0']
TIMESTAMP_URL = 'http://video.google.com/timedtext?lang=en&v={}'

ydl_opts = {
	'outtmpl': 'input_data/wavs/%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

QUOTE = '&quot;'
APOSTROPHE = '&#39;'
NEWLINE = '\n'

def process_data():
	video_data = []
	with open('obama_speeches.csv', 'r', errors='ignore') as input_csv:
		csv_fields = input_csv.readlines()[1:]
		for line in csv_fields:
			csv_arr = line.split(',')
			video_url = csv_arr[0]
			video_start = int(csv_arr[-2])
			video_end = int(csv_arr[-1])

			video_data.append((
				video_url,
				video_start,
				video_end
			))

	return video_data

def process_videos(video_data):
	for (video_url, video_start, video_end) in video_data:
		video_id = video_url[video_url.find('v=') + 2:]
		print('Downloading {}'.format(video_url))
		download_audio(video_url)
		download_timestamp(video_id, video_url)

		print('Creating wavs {}'.format(video_url))
		create_wavs(video_id, video_start, video_end)

		time.sleep(2)

	print('Done.')

def download_audio(video_url):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([video_url])

def download_timestamp(video_id, video_url):
	video_id = video_url[video_url.find('v=') + 2:]
	response = requests.get(TIMESTAMP_URL.format(video_id))
	with open('input_data/timestamps/{}.xml'.format(video_id), 'wb') as xml_output:
		xml_output.write(response.content)

def create_wavs(video_id, video_start, video_end):
	if os.path.exists('output_data/{}'.format(video_id)):
		return

	os.mkdir('output_data/{}'.format(video_id))
	video_wav = AudioSegment.from_wav("input_data/wavs/{}.wav".format(video_id))

	tree = ET.parse('input_data/timestamps/{}.xml'.format(video_id))
	root = tree.getroot()
	wav_text_pairs = []
	for child in root:
		child_text = child.text

		child_text = child_text.encode('ascii', 'ignore').decode('ascii')
		if child_text[0] == '(' and child_text[-1] == ')': # indicates sounds
			continue

		child_start = float(child.attrib['start']) * 1000 # convert to milliseconds
		child_end = child_start + float(child.attrib['dur']) * 1000 # convert to milliseconds

		if child_start < video_start * 60 * 1000:
			continue

		if child_end > video_end * 60 * 1000:
			continue

		child_text = child_text.replace(QUOTE, '')
		child_text = child_text.replace(APOSTROPHE, '\'')
		child_text = child_text.replace(NEWLINE, ' ')

		curr_wav = video_wav[child_start:child_end]
		curr_wav_name = 'output_data/{}/{}.wav'.format(video_id, int(child_start))
		curr_wav.export(curr_wav_name, format='wav')
		wav_text_pairs.append((curr_wav_name, child_text))

	with open('data.txt', 'a') as data_file:
		for (curr_wav_name, curr_child_text) in wav_text_pairs:
			data_file.write('{}|{}\n'.format(curr_wav_name, curr_child_text))


video_data = process_data()
process_videos(video_data)











