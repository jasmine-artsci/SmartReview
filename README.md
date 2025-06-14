# SmartReview

SmartReview is a Python-based graph and sentiment analysis tool built to analyze Amazon product reviews. It constructs a network of reviewers and products to recommend similar products based on shared reviewers, and incorporates sentiment analysis to better understand user opinions.

This version was independently refactored and uploaded by Jasmine Huang for portfolio purposes. It is inspired by a collaborative course project at the University of Toronto (CSC111, Winter 2024).

## Features

- 📦 **Graph Construction**: Builds a bipartite graph between products and reviewers
- 💬 **Sentiment Analysis**: Uses VADER and NLTK to classify review sentiments
- 🔁 **Product Recommendation**: Recommends products based on shared reviewer networks
- 📊 **Visualization**: Uses Seaborn and Matplotlib for interactive visual output (optional)
- 🧠 **Recursive Algorithms**: Calculates average rating and sentiment scores with recursion

---

## 🛠️ Tech Stack

- Python 3.12
- NetworkX
- NLTK + VADER
- NumPy
- Seaborn, Matplotlib (optional)
- JSON for data storage

---

## How to interact with this project?

1. Clone this repo:
git clone https://github.com/jasmine_artsci/SmartReview.git
After cloning the repository, navigate into the project folder:

```bash
cd SmartReview
```

2. **Install Dependencies**  
   Open the `requirements.txt` file in the project directory and install the necessary packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program**  
Execute main.py. This will also download the necessary NLTK resources to enable text analysis features.

4. **Open the Interface**  
Navigate to the interactive window labeled "Product Analysis Display."

5. **Choose a Product**  
Select an ASIN from the dropdown list and click "Select This Product" to load analysis for that item.

6. **Explore the Visualizations**  
After selecting a product, the interface will display the following:

- A dot plot showing Product Ratings Over Time

- A pie chart titled Sentiment of Reviews for [ASIN], summarizing review sentiment distribution

- A list of recommended products based on shared reviewers and sentiment scores

- Sentiment distribution charts for top recommended products

- A word cloud highlighting key terms from reviews of similar products

- A scatter plot showing Average Sentiment for Products Similar to Your Chosen Product

Note: If no similar products are found for the selected ASIN, some graphs may not appear. Simply try another ASIN to explore more results.

7. **Repeat for More Insights**  
Feel free to select different ASINs and click the button again to view data and recommendations for other products. It is encouraged to try out various ASINs to fully explore the tool!

---

## 📬 Contact

For questions, collaboration, or feedback:  
📧 jasminehuangproject@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/jasmine-huang-cs)
