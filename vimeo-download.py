import requests
import base64
from tqdm import tqdm


master_json_url = 'https://173skyfiregce-vimeo.akamaized.net/exp=1536825658~acl=%2F241576972%2F%2A~hmac=fe580db248523824bfed57f73a80bac8c25a7991bbc5c6d529397df3019af3e9/241576972/sep/video/866588646,866588648,866588638/master.json?base64_init=1'
base_url = master_json_url[:master_json_url.rfind('/', 0, -26) + 1]

resp = requests.get(master_json_url)
content = resp.json()

heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
idx, _ = max(heights, key=lambda (_, h): h)
video = content['video'][idx]
video_base_url = base_url + video['base_url']
print 'base url:', video_base_url

filename = 'video_%d.mp4' % video['id']
print 'saving to %s' % filename

video_file = open(filename, 'wb')

init_segment = base64.b64decode(video['init_segment'])
video_file.write(init_segment)

for segment in tqdm(video['segments']):
    segment_url = video_base_url + segment['url']
    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print 'not 200!'
        print resp
        print segment_url
        break
    for chunk in resp:
        video_file.write(chunk)

video_file.flush()
video_file.close()
