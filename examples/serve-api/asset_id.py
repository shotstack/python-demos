import sys
import shotstack_sdk as shotstack
import os

from shotstack_sdk.api import serve_api

if __name__ == "__main__":
    host = "https://api.shotstack.io/serve/stage"

    if os.getenv("SHOTSTACK_SERVE_HOST") is not None:
        host =  os.getenv("SHOTSTACK_SERVE_HOST")

    configuration = shotstack.Configuration(host = host)

    if os.getenv("SHOTSTACK_KEY") is None:
        sys.exit("API Key is required. Set using: export SHOTSTACK_KEY=your_key_here")  

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = serve_api.ServeApi(api_client)

        id = sys.argv[1]

        if id is None:
            sys.exit(">> Please provide the UUID of the render (i.e. python examples/serve-api/asset_id.py 2abd5c11-0f3d-4c6d-ba20-235fc9b8e8b7)\n")  

        try:
            api_response = api_instance.get_asset(id)

            data = api_response['data']

            if data['attributes']['status'] == "failed":
                print(">> Something went wrong, asset could not be copied.")
            else:
                print(f">> Asset CDN URL: {data['attributes']['url']}")
                print(f">> Asset ID:  {data['attributes']['id']}")
                print(f">> Render ID:  {data['attributes']['render_id']}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")