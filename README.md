# Simple Serverless Flux Handler for RunPod

Implements a Dockerfile for creating a simple serverless Flux  handler for RunPod.

The Dockerfile attempts to preload the model to include it in the image.

# How to Test

```python
import requests
import base64
from PIL import Image
from io import BytesIO

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
}

data = {
    'input': {"prompt":"A fish holding a sign that says Hello"}
}

print("Calling...")

response = requests.post('https://api.runpod.ai/v2/YOUR_API/runsync', headers=headers, json=data)

# Get the JSON response
response_json = response.json()

# Assume a successful request
image_str = response_json["output"]["image_url"]

# Remove the "data:image/png;base64," prefix
header, base64_data = image_str.split(',', 1)

# Decode the base64 string
image_bytes = base64.b64decode(base64_data)

# Convert to PIL Image
image = Image.open(BytesIO(image_bytes))

# Save the image to disk
image.save("output.png")
```

![A fish holding a sign that says Hello](output.png)
