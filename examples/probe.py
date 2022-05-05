import sys
import shotstack_sdk as shotstack
import os

from shotstack_sdk.api import edit_api

if __name__ == "__main__":
    host = "https://api.shotstack.io/stage"

    if os.getenv("SHOTSTACK_HOST") is not None:
        host =  os.getenv("SHOTSTACK_HOST")

    configuration = shotstack.Configuration(host = host)

    if os.getenv("SHOTSTACK_KEY") is None:
        sys.exit("API Key is required. Set using: export SHOTSTACK_KEY=your_key_here")  

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        url = sys.argv[1]

        if url is None:
            sys.exit(">> Please provide the URL to a media file to inspect (i.e. python examples/probe.py https://github.com/shotstack/test-media/raw/main/captioning/scott-ko.mp4)\n")  
            
        try:
            api_response = api_instance.probe(url)

            streams = api_response['response']['metadata']['streams']
            
            for stream in streams:
                if stream['codec_type'] == "video":
                    print(f"Example settings for:  {api_response['response']['metadata']['format']['filename']}")
                    print(f"Width: {stream['width']}px")
                    print(f"Height: {stream['height']}px")
                    print(f"Framerate: {stream['r_frame_rate']} fps")
                    print(f"Duration: {stream['duration']} secs")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")