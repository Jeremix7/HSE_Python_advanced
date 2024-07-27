| Name of the project | Goals | Results |
| :--- | :--- | :--- |
| CountVectorizer | Write a class for vectorizing strings | Implemented class CountVectorizer:
- f​it  -  build a dictionary "token to index" from the input corpus and save it as an attribute of the class;
- transform  -  transform a new corpus based on a saved dictionary, should return a list of lists. If some token from the new corpus is not represented in the dictionary, then you need to ignore it;
- f​it_transform  -  fit and transform on the same corpus, should return a list of lists. |
| InvertedIndex | Develop a comprehensive solution centered around the concept of an "Inverted Index". |  Implemented the function load_document. Implemented the function build_inverted_index. Implemented methods init and query for the class InvertedIndex. Added a command line interface. | 
