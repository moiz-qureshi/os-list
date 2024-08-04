import requests
from bs4 import BeautifulSoup

def scrape_github_trending():
    url = 'https://github.com/trending?since=daily'
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')

    projects = []
    for repo in soup.find_all('article', class_='Box-row'):
        title_tag = repo.find('h1', class_='h3 lh-condensed')
        if title_tag is None:
            print("Title tag not found for a project. Skipping...")
            continue

        link_tag = title_tag.find('a')
        if link_tag is None:
            print("Link tag not found for a project. Skipping...")
            continue

        project_link = link_tag['href'].strip()
        project_name = link_tag.text.strip()
        
        description_tag = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
        project_description = description_tag.text.strip() if description_tag else "No description provided"

        projects.append({
            'name': project_name,
            'description': project_description,
            'link': f'https://github.com{project_link}'
        })

    return projects

def generate_html_report(projects):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending Projects</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333333;
        }
        .project {
            margin-bottom: 15px;
            padding: 10px;
            border-bottom: 1px solid #dddddd;
        }
        .project:last-child {
            border-bottom: none;
        }
        .project-name {
            font-size: 18px;
            font-weight: bold;
        }
        .project-description {
            margin: 5px 0;
            color: #666666;
        }
        .project-link {
            color: #007bff;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GitHub Trending Projects</h1>
        {project_entries}
    </div>
    <script>
        // JavaScript for interactive features can be added here
    </script>
</body>
</html>
"""

    project_entries = ''
    for project in projects:
        project_entries += f"""
        <div class="project">
            <div class="project-name">
                <a href="{project['link']}" class="project-link" target="_blank">{project['name']}</a>
            </div>
            <div class="project-description">{project['description']}</div>
        </div>
        """

    return html_content.format(project_entries=project_entries)

def main():
    try:
        projects = scrape_github_trending()
        if not projects:
            print("No projects found. Please check the page structure or URL.")
            return

        html_report = generate_html_report(projects)

        with open('report.html', 'w', encoding='utf-8') as file:
            file.write(html_report)

        print("HTML report generated successfully.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")

if __name__ == '__main__':
    main()
