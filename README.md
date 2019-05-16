### Obama Speech Dataset

#### Running The Script
The dataset here contains Obama's speeches from `The Obama White House` YouTube channel.

To run the script, first install [FFmpeg](ffmpeg.org) on your operating system. Then run

```
pip3 install -r requirements.txt
python process.py
```

#### Script Overview
The script iterates through `obama_speeches.csv`, fetches each YouTube video, uses FFmpeg to convert it to audio. It then fetches the corresponding timestamps. Both are stored in the `input_data` directory.

Later, it creates a folder with the `VIDEO_ID` as the directory name in `output_data` and splices the data into a bunch of wav files. Each wav file is written into `data.txt` in the form `output_data/video_id/\d+.wav|text of the wav.`

#### Post Processing
Run `trim.py` to create train/val files from data.txt.