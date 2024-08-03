# src/db/__init__.py

# Import models
from .models.document import Document
from .models.literature import Literature
from .models.users import Users
from .models.interaction import Interaction

# Import CRUD operations
# from .CRUD import document_crud, literature_crud, user_crud, interaction_crud, embedding_crud
from .CRUD.document_crud import DocumentCRUD
from .CRUD.literature_crud import LiteratureCRUD
from .CRUD.interaction_crud import InteractionCRUD
from .CRUD.user_crud import UsersCRUD
# from db.CRUD.document_crud import DocumentCRUD
# from .CRUD.embedding_crud import EmbeddingsCRUD
