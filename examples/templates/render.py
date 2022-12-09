import shotstack_sdk as shotstack
import os
import sys

from shotstack_sdk.api import edit_api
from shotstack_sdk.model.template_render import TemplateRender
from shotstack_sdk.model.merge_field import MergeField


if __name__ == '__main__':
    host = 'https://api.shotstack.io/stage'

    if os.getenv('SHOTSTACK_HOST') is not None:
        host =  os.getenv('SHOTSTACK_HOST')

    configuration = shotstack.Configuration(host = host)

    if os.getenv('SHOTSTACK_KEY') is None:
        sys.exit('API Key is required. Set using: export SHOTSTACK_KEY=your_key_here')  

    configuration.api_key['DeveloperKey'] = os.getenv('SHOTSTACK_KEY')

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        id = sys.argv[1]

        if id is None:
            sys.exit(">> Please provide the UUID of the template (i.e. python examples/templates/render.py 7feabb0e-b5eb-8c5e-847d-82297dd4802a)\n")

        merge_field_url = MergeField(
            find = 'URL',
            replace = 'https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/footage/skater.hd.mp4'
        )

        merge_field_trim = MergeField(
            find = 'TRIM',
            replace = 3
        )

        merge_field_length = MergeField(
            find = 'LENGTH',
            replace = 6
        )

        template = TemplateRender(
            id = id,
            merge = [
                merge_field_url,
                merge_field_trim,
                merge_field_length
            ]
        )

        try:
            api_response = api_instance.post_template_render(template)

            message = api_response['response']['message']
            id = api_response['response']['id']
        
            print(f"{message}\n")
            print(">> Now check the progress of your render by running:")
            print(f">> python examples/status.py {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")
