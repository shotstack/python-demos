import shotstack_sdk as shotstack
import os

from shotstack_sdk.api                          import edit_api
from shotstack_sdk.model.clip                   import Clip
from shotstack_sdk.model.track                  import Track
from shotstack_sdk.model.timeline               import Timeline
from shotstack_sdk.model.output                 import Output
from shotstack_sdk.model.edit                   import Edit
from shotstack_sdk.model.video_asset            import VideoAsset
from shotstack_sdk.model.rotate_transformation  import RotateTransformation
from shotstack_sdk.model.skew_transformation    import SkewTransformation
from shotstack_sdk.model.flip_transformation    import FlipTransformation
from shotstack_sdk.model.transformation         import Transformation

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

        video_asset = VideoAsset(
            src = "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/footage/skater.hd.mp4"
        )

        rotate = RotateTransformation(
            angle = 45
        )

        skew = SkewTransformation(
            x = 0.25,
            y = 0.1
        )

        flip = FlipTransformation(
            horizontal = True,
            vertical = True
        )

        transformation = Transformation(
            rotate  = rotate,
            skew    = skew,
            flip    = flip
        )

        video_clip = Clip(
            asset  = video_asset,
            start  = 0.0,
            length = 8.0,
            scale  = 0.6,
            transform = transformation
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