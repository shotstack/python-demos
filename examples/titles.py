import shotstack_sdk as shotstack
import os

from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.transition  import Transition
from shotstack_sdk.model.title_asset import TitleAsset

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

        styles = [
            "minimal",
            "blockbuster",
            "vogue",
            "sketchy",
            "skinny",
            "chunk",
            "chunkLight",
            "marker",
            "future",
            "subtitle"
        ]

        clips = []
        start = 0.0
        length= 3.0

        soundtrack = Soundtrack(
            src     = "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/music/dreams.mp3",
            effect  = "fadeInFadeOut"
        )

        for style in styles:
            title = TitleAsset(
                text = style,
                style= style,
                size = "small"
            )

            transition = Transition(
                _in="fade",
                out="fade"
            )

            clip = Clip(
                asset      = title,
                length     = length,
                start      = start,
                transition = transition,
                effect     = 'zoomIn'
            )

            start = start + length

            clips.append(clip)

            
        track = Track(clips=clips)

        timeline = Timeline(
            background = "#000000",
            soundtrack = soundtrack,
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