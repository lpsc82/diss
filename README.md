# Repositório da minha dissertação de mestrado. 
Código em Python, desenvolvido a partir de outro já existente, da autoria de Gil Domingues.

## Pasta Dataset: 
Dataset separado nos dados obtidos nas fases I e II

## Pasta Source: 
Código desenvolvido

### get_dataset_lang.py
Gera o dataset a partir da lista de artigos mais populares em saúde da Wikipédia

### ApiInterface
Faz pedidos à API de wikimedia. Insere os dados na base de dados com a ajuda do DatabaseInterface.py.

### DatabaseInterface.py
Trata da conexão com a base de dados.

### DatasetProcessor.py
Processa cada artigo presente no dataset, a partir do seu titulo, recorrendo a ApiInterface

### GetAdmins.py
Atualiza os utilizadores admin na base de dados a partir da lista de admins.

### CheckBrokenArticles.py
Regista artigos que não existem: a partir dos links, mesmo os que não estão no dataset mas apareceram na base de dados como links.

### CleanWikitextContent.py
Escreve o conteúdo de um artigo para um ficheiro em formato wikitext.
Remove o markdown e escreve o texto limpo noutro ficheiro.
Calcula os valores de Flesch e Kincaid (legibilidade), assim como a length do artigo.

### ParseImagesFromWikitext.py
Obtém o número de assets que são imagens, usando o conteúdo wikitext.

### CSVGen.py
Calcula as métricas e escreve-as num ficheiro CSVGen.csv.

### VolatilityCalc.py
Calcula a volatilidade dos artigos e escreve os resultados num ficheiro volatility.csv.


### GetWpAdmins.py
Regista os utilizadores que fazem parte da lista de administradores do WikiProject Medicine.

### GetTranslated.py
Regista os artigos que estão presentes na lista de artigos traduzidos pela Health Translation TaskForce.

### GetSections.py
Regista as secções dos artigos que fazem parte da lista de secções recomendadas pelo WikiProject Medicine.

### GetReputatedLinks.py
Regista os links que estão na lista de hiperligações sugeridas pelo National Institute of Health.

### GatherMedicineTemplates.py
Cria ficheiro com todos os templates de medicina relevantes.

### GatherMedicineTemplates.py
Cria ficheiro com todos os templates de medicina relevantes. Implementado para todas as línguas, embora só tenha sido utlizado/testado o inglês.

### ParseTemplatesFromContent.py
Carrega os templates de medicina na base de dados.
Desenvolvido para outrso idiomas além do inglês, mas só este foi usado/testado.

### ParseMedicalInfoboxValues.py
Insere os valores de infobox médica na base de dados.

### PutInfoboxInDatabase.py
Coloca todas as infoboxes relevantes na base de dados.

### StripInfoFromContent.py
Obtém o número de tabelas no artigo. - não usado/testado.
Insere os indices médicos na base de dados.

### CategoryUpdate.py
Insere categorias dos artigos analisados na base de dados e cria os links entre artigos - categorias.

### GetAssess
Insere a classificação dos artigos segundo as listas de avaliação do WikiProject Medicine.

### GenerateMedicineMetrics.py
Calcula as métricas e medidas especificas, propostas, e escreve os resultados num ficheiro medicine_metrics.csv.
