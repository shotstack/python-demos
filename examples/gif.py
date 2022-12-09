import shotstack_sdk as shotstack
import os

from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.shotstack_destination import ShotstackDestination

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

        images = [
            "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/examples/images/pexels/pexels-photo-712850.jpeg",
            "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/examples/images/pexels/pexels-photo-867452.jpeg",
            "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/examples/images/pexels/pexels-photo-752036.jpeg"
        ]

        clips = []
        start = 0.0
        length = 1.5

        soundtrack = Soundtrack(
            src = "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/music/gangsta.mp3",
            effect = "fadeInFadeOut"
        )

        for image in images:
            imageAsset = ImageAsset(src = image)

            clip = Clip(
                asset = imageAsset,
                start = start,
                length = length,
                effect = "zoomIn"
            )

            start = start + length
            clips.append(clip)

        track = Track(clips = clips)

        timeline = Timeline(
            background = "#000000",
            soundtrack = soundtrack,
            tracks = [track]
        )

        output = Output(
            format = "gif",
            resolution = "preview",
            fps = 12,
            repeat = False
        )

        edit = Edit(
            timeline = timeline,
            output = output
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
