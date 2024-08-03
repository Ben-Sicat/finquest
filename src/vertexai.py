from google.cloud import aiplatform_v1
import os
from dotenv import load_dotenv
import vertexai

load_dotenv()

def initialize_vertex_ai():
  """Initializes the Vertex AI client with credentials from the environment variable."""

  # Check if the environment variable is set
  if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    raise EnvironmentError(
        "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set"
    )
  vertexai.init(project ="finquest", location = "us-central1")
  # Create the Vertex AI client
  client = aiplatform_v1.ModelServiceClient()
  if not client:
    raise Exception("Could not initialize Vertex AI client")
  else:
      print("Vertex AI client initialized successfully.")
  return client
if __name__ == "__main__":
    initialize_vertex_ai()
