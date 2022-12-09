import shotstack_sdk as shotstack
import os
import sys

from shotstack_sdk.api import edit_api
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
from shotstack_sdk.model.template import Template


if __name__ == '__main__':
    host = 'https://api.shotstack.io/stage'

    if os.getenv('SHOTSTACK_HOST') is not None:
        host = os.getenv('SHOTSTACK_HOST')

    configuration = shotstack.Configuration(host = host)

    if os.getenv('SHOTSTACK_KEY') is None:
        sys.exit('API Key is required. Set using: export SHOTSTACK_KEY=your_key_here')  

    configuration.api_key['DeveloperKey'] = os.getenv('SHOTSTACK_KEY')

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        video_asset = VideoAsset(
            src = '{{ URL }}',
            trim = '{{ TRIM }}'
        )

        video_clip = Clip(
            asset = video_asset,
            start = 0.0,
            length = '{{ LENGTH }}'
        )

        track = Track(clips=[video_clip])

        timeline = Timeline(
            background = '#000000',
            tracks = [track]
        )

        output = Output(
            format = 'mp4',
            resolution = 'sd'
        )

        edit = Edit(
            timeline = timeline,
            output = output
        )

        template = Template(
            name = 'Trim Template',
            template = edit
        )

        try:
            api_response = api_instance.post_template(template)

            message = api_response['response']['message']
            id = api_response['response']['id']

            print(f"{message}\n")
            print(">> Now render the template using the id:")
            print(f">> python examples/templates/render.py {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")
