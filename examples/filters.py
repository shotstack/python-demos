import shotstack_sdk as shotstack
import os

from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.video_asset import VideoAsset
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

        filters = [
            "original",
            "boost",
            "contrast",
            "muted",
            "darken",
            "lighten",
            "greyscale",
            "negative"
        ]

        video_clips = []
        title_clips = []
        start       = 0.0
        length      = 3.0
        trim        = 0.0
        end         = length

        soundtrack = Soundtrack(
            src     = "https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/music/freeflow.mp3",
            effect  = "fadeInFadeOut"
        )

        for _filter in filters:
            #Video clips
            video_asset = VideoAsset(
                src = 'https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/footage/skater.hd.mp4',
                trim= trim
            )

            video_clip = Clip(
                asset = video_asset,
                start = start,
                length= length
            )

            if _filter != "original":
                video_transition = Transition(_in="wipeRight")

                video_clip['transition'] = video_transition
                video_clip['filter']     = _filter
                video_clip['length']     = length + 1

            video_clips.append(video_clip)

            #Title clips
            title_transition = Transition(
                _in="fade",
                out="fade"
            )

            title_asset = TitleAsset(
                text = _filter,
                style= "minimal",
                size = "x-small"
            )

            title_clip = Clip(
                asset      = title_asset,
                length     = length - (1 if start == 0 else 0),
                start      = start,
                transition = title_transition
            )

            title_clips.append(title_clip)

            trim  = end - 1
            end   = trim + length + 1
            start = trim

        track_1 = Track(clips=title_clips)

        track_2 = Track(clips=video_clips)

        timeline = Timeline(
            background = "#000000",
            soundtrack = soundtrack,
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