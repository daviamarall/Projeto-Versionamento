import json
import os
import markdown2
from jinja2 import Environment, FileSystemLoader

# Carregar dados do arquivo JSON
with open("data.json", "r") as file:
    data = json.load(file)

# Configurar o ambiente Jinja2
env = Environment(loader=FileSystemLoader("templates"))
index_template = env.get_template("index.html")
post_template = env.get_template("post.html")

# Processar cada postagem
for post in data:
    # Usar o título da postagem como parte do caminho do arquivo Markdown
    title_for_filename = post.get("title", "").lower().replace(' ', '_')
    markdown_file_path = f"mddir/{title_for_filename}.md"

    # Ler conteúdo do arquivo Markdown
    if os.path.exists(markdown_file_path):
        with open(markdown_file_path, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()

        # Converter Markdown para HTML
        html_content = markdown2.markdown(markdown_content)

        # Renderizar a postagem usando o template
        rendered_post = post_template.render(
            title=post["title"],
            description=post["description"],
            author=post["author"],
            content=html_content
        )

        # Salvar a postagem como um arquivo HTML
        output_filename = f"output/{post['title'].replace(' ', '_')}.html"
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_post)

        print(f"Postagem gerada: {output_filename}")
    else:
        print(f"Arquivo Markdown não encontrado: {markdown_file_path}")

# Renderizar a página inicial
rendered_index = index_template.render(posts=data)
with open("output/index.html", "w", encoding="utf-8") as index_file:
    index_file.write(rendered_index)

print("Blog atualizado com sucesso!")
