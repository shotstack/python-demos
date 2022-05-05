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
    host = "https://api.shotstack.io/stage"

    if os.getenv("SHOTSTACK_HOST") is not None:
        host =  os.getenv("SHOTSTACK_HOST")

    configuration = shotstack.Configuration(host = host)

    if os.getenv("SHOTSTACK_KEY") is None:
        sys.exit("API Key is required. Set using: export SHOTSTACK_KEY=your_key_here")  

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        ONE_FRAME = 1/25

        # Setup the main background clip
        background_asset = VideoAsset(
            src = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/examples/picture-in-picture/code.mp4"
        )

        background_clip = Clip(
            asset   = background_asset,
            start   = 5.0,
            length  = 10.0 
        )

        background_track = Track(clips=[background_clip])

        # Setup the overlay picture in picture clip
        # 1. Full screen
        overlay_asset_1 = VideoAsset(
            src    = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/examples/picture-in-picture/commentary.mp4",
            volume = 1.0
        )

        overlay_clip_1 = Clip(
            asset   = overlay_asset_1,
            start   = 0.0,
            length  = 5.0 - ONE_FRAME
        )

        # 2. Bottom right picture in picture after 5 seconds
        overlay_asset_2 = VideoAsset(
            src  = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/examples/picture-in-picture/commentary.mp4",
            volume = 1.0,
            trim   = 5.0
        )

        overlay_clip_2 = Clip(
            asset   = overlay_asset_2,
            start   = 5.0,
            length  = 5.0 - ONE_FRAME,
            scale   = 0.35,
            position= "bottomRight"
        )

        # 3. Top right picture in picture after 10 seconds
        overlay_asset_3 = VideoAsset(
            src    = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/examples/picture-in-picture/commentary.mp4",
            volume = 1.0,
            trim   = 10.0
        )

        overlay_clip_3 = Clip(
            asset   = overlay_asset_3,
            start   = 10.0,
            length  = 2.5 - ONE_FRAME,
            scale   = 0.35,
            position= "topRight"
        )

        # 4. Small bottom right picture in picture after 12.5 seconds
        overlay_asset_4 = VideoAsset(
            src    = "https://shotstack-assets.s3.ap-southeast-2.amazonaws.com/examples/picture-in-picture/commentary.mp4",
            volume = 1.0,
            trim   = 12.5
        )

        overlay_clip_4 = Clip(
            asset   = overlay_asset_4,
            start   = 12.5,
            length  = 2.5,
            scale   = 0.25,
            position= "topRight"
        )

        overlay_track = Track(clips=[
            overlay_clip_1, overlay_clip_2, overlay_clip_3, overlay_clip_4
        ])

        timeline = Timeline(
            background = "#000000",
            tracks     = [overlay_track, background_track]
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
        
            print("message\n")
            print(">> Now check the progress of your render by running:")
            print(f">> python examples/status.py {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")