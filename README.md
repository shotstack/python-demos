# Shotstack Python Examples

### Video examples

- **text.py** -
    Create a HELLO WORLD video title against black background with a zoom in motion effect and soundtrack.

- **images.py** -
    Takes an array of image URLs and creates a video with a soundtrack and simple zoom in effect.

- **titles.py** -
    Create a video to demo titles using the available preset font styles, a soundtrack, zoom in motion effect and 
    wipe right transition.

- **trim.py** -
    Trim the start and end of a video clip to output a shortened video.

- **filters.py** -
    Applies filters to a video clip, including a title with the name of the filter and a soundtrack.

- **picture-in-picture.py** -
    Layer a small foreground clip, using position and scale, over a fullscreen background clip, to create a picture 
    in picture effect.

- **merge.py** -
    Merge data in to a video using merge fields.

- **transform.py** -
    Apply transformations (rotate, skew and flip) to a video clip.
    
### Image examples

- **border.py** -
    Add a border frame around a background photo.

- **gif.py** -
    Create an animated gif that plays once.

### Template examples

- **templates/create.py** -
    Save an edit as a re-usable template with placeholders.

- **templates/render.py** -
    Render a template using merge fields to replace placeholders.

### Polling example

- **status.py** -
    Shows the status of a render task and the output video URL. Run this after running one of the render examples.

### Probe example

- **probe.py** -
    Fetch metadata for any media asset on the internet such as width, height, duration, etc...

### Asset management examples

- **serve-api/render_id.py** -
    Fetch all assets associated with a render ID. Includes video or image and thumbnail and poster.

- **serve-api/asset_id.py** -
    Fetch an individual asset by asset ID.

- **serve-api/destination.py** -
    Shows how to exclude a render from being sent to the Shotstack hosting destination.

- **mux.py** -
    Sends a rendered video to Mux hosting and excludes it from Shotstack. Requires a Mux account.

### Installation

Install the required dependencies including the [Shotstack Python SDK](https://www.npmjs.com/package/shotstack-sdk)

```bash
pip install -r requirements.txt
```

### Set your API key

The demos use the **staging** endpoint by default so use your provided **staging** key:

```bash
export SHOTSTACK_KEY=your_key_here
```

Windows users (Command Prompt):

```bash
set SHOTSTACK_KEY=your_key_here
```

You can [get an API key](http://shotstack.io/?utm_source=github&utm_medium=demos&utm_campaign=[python_sdk) via the 
Shotstack web site.

### Run an example

The examples directory includes a number of examples demonstrating the capabilities of the 
Shotstack API.

#### Rendering

To run a rendering/editing example run the examples at the root of the examples folder, e.g. to run the images video 
example:

```bash
python examples/images.py
```

#### Polling

To check the status of a render, similar to polling run the `status.py` example with the render ID, e.g.:

```bash
python examples/status.py 8b844085-779c-4c3a-b52f-d79deca2a960
```

#### Asset management

To look up assets hosted by Shotstack run the examples in the [examples/serve-api](./examples/serve-api/) directory.

Find assets by render ID:
```bash
python examples/serve-api/render_id.py 8b844085-779c-4c3a-b52f-d79deca2a960
```

or 

Find an asset by asset ID:
```bash
python examples/serve-api/asset_id.py 3f446298-779c-8c8c-f253-900c1627b776
```
