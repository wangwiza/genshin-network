# Genshin Network

Genshin Network is a Python-based project that scrapes data from the Genshin Impact wiki to generate a character relationship network graph. This tool helps visualize the connections between the diverse cast of characters in the popular game, Genshin Impact.

-----

## 🌟 Features

  * **Web Scraping**: Utilizes Selenium and BeautifulSoup to automatically extract character data from the Genshin Impact wiki.
  * **Data Transformation**: Processes the raw scraped data into a structured format suitable for network analysis.
  * **Network Analysis**: Analyzes the character relationships to build a network graph.
  * **Interactive Visualization**: Displays the character network graph in a web interface using Flask.

-----

## 🛠️ Tech Stack

  * **Python**: The core programming language for the project.
  * **Selenium**: Used for web scraping dynamic web pages.
  * **BeautifulSoup4**: For parsing HTML and XML documents.
  * **Pandas**: For data manipulation and analysis.
  * **Flask**: A lightweight web framework for displaying the network graph.
  * **HTML/CSS/JavaScript**: For the frontend visualization.

-----

## 🚀 Getting Started

To get started with Genshin Network, you'll need to have Python installed on your system.

### **Installation**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/wangwiza/genshin-network.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd genshin-network
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -r scraper/requirements.txt
    ```

-----

## ⚙️ How It Works

The project is divided into three main parts:

1.  **Extraction**: The `scraper/extract.py` script uses Selenium to browse the Genshin Impact wiki and extract character information.
2.  **Transformation**: The `scraper/transforms.py` script takes the raw scraped data and cleans it, preparing it for analysis.
3.  **Analysis & Visualization**: The `scraper/analysis.py` script processes the transformed data to build the network graph. The resulting data is then served by a Flask application, and the `index.html` file provides the frontend for the visualization.

To run the full pipeline, execute the following commands in order:

```bash
python scraper/extract.py
python scraper/transforms.py
python scraper/analysis.py
```

After running the scripts, you can start the Flask server to see the visualization.

-----

## 🖼️ Visualization

![Genshin Character Dialogue Mention Network](https://github.com/wangwiza/genshin-network/blob/main/visuals/network_but_smaller.png)
The two biggest central nodes are Paimon (left) and Aether/Traveler (right)

-----

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.


