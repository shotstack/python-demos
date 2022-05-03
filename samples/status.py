import sys
import shotstack_sdk as shotstack
import os

from shotstack_sdk.api import edit_api

if __name__ == "__main__":
    configuration = shotstack.Configuration(
        host = "https://api.shotstack.io/v1"
    )

    if os.getenv("SHOTSTACK_KEY") is None:
        sys.exit("API Key is required. Set using: export SHOTSTACK_KEY=your_key_here")  

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        id = sys.argv[1]

        if id is None:
            sys.exit(">> Please provide the UUID of the render task (i.e. python examples/status.py 2abd5c11-0f3d-4c6d-ba20-235fc9b8e8b7)\n")  

        apiUrl = "https://api.shotstack.io/stage"

        if os.getenv("SHOTSTACK_HOST") is not None:
            apiUrl =  os.getenv("SHOTSTACK_HOST")

        api_response = api_instance.get_render(id, data=False, merged=True)

        #print(api_response['response'])

        status = api_response['response']['status']
        url    = api_response['response']['url']

        print('Status: ' + status.upper() + '\n')

        if status == "done":
            print(f">> Asset URL: {url}")
        elif status == 'failed':
            print(">> Something went wrong, rendering has terminated and will not continue.")
        else:
            print(">> Rendering in progress, please try again shortly.\n>> Note: Rendering may take up to 1 minute to complete."")