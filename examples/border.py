import shotstack_sdk as shotstack
import os

from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit

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

        border_asset = ImageAsset(
            src     = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/borders/80s-acid-pink-square.png"
        )

        border_clip = Clip(
            asset   = border_asset,
            start   = 0.0,
            length  = 1.0
        )

        track_1 = Track(clips = [border_clip])

        image_asset = ImageAsset(src = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/images/dolphins.jpg")

        image_clip = Clip(
            asset   = image_asset,
            start   = 0.0,
            length  = 1.0
        )

        track_2 = Track(clips = [image_clip])

        timeline = Timeline(
            background = "#000000",
            tracks     = [track_1, track_2]
        )

        output = Output(
            format      = "mp4",
            resolution  = "sd",
            fps         = 30.0
        )

        edit = Edit(
            timeline = timeline,
            output   = output
        )

        try:
            api_response = api_instance.post_render(edit)

            message = api_response['response']['message']
            id = api_response['response']['id']
        
            print(f"{message}\n")
            print(">> Now check the progress of your render by running:")
            print(f">> python examples/status.py {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")