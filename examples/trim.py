import shotstack_sdk as shotstack
import os

from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.video_asset import VideoAsset

if __name__ == "__main__":
    configuration = shotstack.Configuration(
        host = "https://api.shotstack.io/v1"
    )

    if os.getenv("SHOTSTACK_KEY") is None:
        sys.exit("API Key is required. Set using: export SHOTSTACK_KEY=your_key_here")  

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")
    
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        video_asset = VideoAsset(
            src = "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/footage/skater.hd.mp4",
            trim = 3.0
        )

        video_clip = Clip(
            asset = video_asset,
            start = 0.0,
            length= 8.0
        )

        track = Track(clips=[video_clip])

        timeline = Timeline(
            background = "#000000",
            tracks     = [track]
        )

        output = Output(
            format      = "mp4",
            resolution  = "sd"
        )

        edit = Edit(
            timeline = timeline,
            output   = output
        )

        api_response = api_instance.post_render(edit)

        message = api_response['response']['message']
        id = api_response['response']['id']
    
        print("message\n")
        print(">> Now check the progress of your render by running:")
        print(f">> python examples/status.py {id}")