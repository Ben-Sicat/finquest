from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import logging
import vertexai
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextEmbedder:
    """
    A class to handle text embedding using a pre-trained Vertex AI model.
    """
    vertexai.init(project="finquest", location="us-central1")

    def __init__(
        self,
        project: str = "finquest",
        model_name: str = "text-embedding-004",
        dimensionality: Optional[int] = 256,
        task: str = "RETRIEVAL_DOCUMENT"
    ):
        """
        Initialize the TextEmbedder with model configurations.

        Args:
            model_name (str): The name of the embedding model to use.
            dimensionality (Optional[int]): Desired output dimensionality of embeddings.
            task (str): The task type for embeddings, default is 'RETRIEVAL_DOCUMENT'.
        """
        self.project_ID = project
        self.model_name = model_name
        self.dimensionality = dimensionality
        self.task = task
        self.model = TextEmbeddingModel.from_pretrained(self.model_name)
    
    def __call__(self, text: str) -> List[float]:
        """
        Embed a single text string.

        Args:
            text (str): The text string to embed.

        Returns:
            List[float]: The embedding vector for the input text.
        """
        try:
            input = TextEmbeddingInput(text=text)
            kwargs = {'output_dimensionality': self.dimensionality} if self.dimensionality else {}
            embedding = self.model.get_embeddings([input], **kwargs)[0] # Get the first (and only) embedding
            return embedding.values
        except Exception as e:
            logging.error(f"An error occurred while generating the embedding: {e}")
            raise RuntimeError(f"Failed to embed text: {e}")
        #now we laso have to handle the case where the text is a list 
        
# Example Usage
if __name__ == "__main__":
    embedder = TextEmbedder()
    embedding = embedder("This is a test sentence.")
    print(embedding)