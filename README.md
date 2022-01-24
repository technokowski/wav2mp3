# wav2mp3
Simple Flask site to upload and convert wav files to mp3 files.

Why? I realize there are many utilities to do this, both online and local. 
I have a very specific reason; it's for my Dad.

He writes music on his iPhone, and the only format his program (spire studio) will export to is .wav.
He likes to share his projects with others, and wav files are too big. He has been uploading them to a
file share, and then I convert them to .mp3. But, I wanted to give him the power to do it himself, 
so I made this. It works flawlessly for him, which is the only criteria. 

You could easily expand this and add other file conversion formats, as it is utilizing the pydub library,
which is excellent and very comprehensive. 

Please feel free to criticize the code, as my main goal was to get it up and running quickly. 
