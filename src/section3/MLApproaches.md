# Section 3: Machine Learning Engineering

## 3.1 Feature Engineering

### Understanding TikTok’s Wild Format

TikTok thrives on being spontaneous and variety. Users can build content around trending sounds, memes, dance challenges, or even remix other TikToks. This open-ended format fuels creativity—but also creates a noisy, unpredictable dataset that's hard to categorize.

### Better Video Categorization

To make sense of this variety, we need smarter video categorization. The current method we did—labeling videos as “animals” or “others”—is far too limited and usually relies on a single hashtag. Instead, we can use clustering based on hashtags and video descriptions to capture more meaningful content themes.

A better method would involve clustering hashtags and video descriptions to create more nuanced categories that better reflect a video's actual content.

Here's how I'd approach categorizing videos more effectively:

1. Tokenization & Text Processing

   - We'll need to break down video descriptions into individual words (tokens), remove punctuation, and normalize the text by converting it all to lowercase
   - Hashtags are especially important on TikTok, so they should be split and analyzed separately
   - There are various text processing libraries for this, but the most cited ones are NLTK (https://www.nltk.org/) and spaCy (https://spacy.io/)
   - NLTK is great for basic tokenization and filtering
   - spaCy is faster and more production-ready, with features like Named Entity Recognition (NER), which can help detect brands, products, or other buzzwords

   Given the nature of TikTok content, spaCy is likely the better choice for building features from descriptions and hashtags

2. Creating Better Categories

   - Instead of just "animals" vs "other," we could use topic modeling techniques like Latent Dirichlet Allocation (LDA) to discover natural, underlying content categories
   - Using word embeddings can capture the similarities between words and hashtags. How does this help? This helps in grouping the similar or related hashtags even when they're not completely the same. For example, #baking, #desserttok, and #fypcooking aren't literally the same text, but they have the same context. This gives us a generally more informative way of describing videos
   - This kind of categorization would provide much richer, context-aware labels

### Sentiment Analysis

Sentiment analysis could be a highly valuable signal, even when limited to text-based features like descriptions and hashtags

1. Challenging but worth it

   - A driving force of short-form videos is its emotional impact
   - TikTok descriptions are short, emoji-heavy, and filled with slang which may prove to be difficult to analyze for traditional sentiment tools
   - Even not-so-accurate sentiment detection could still prove to be useful in how the textual tone influences popularity

2. Practical Approach

   - We could use VADER (https://github.com/cjhutto/vaderSentiment) which is designed specifically for social media content and handles emojis pretty well
   - For a more modern approach, fine-tuned versions of RoBERTa (https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) trained on Twitter data work surprisingly well on TikTok content too
   - We could also create custom features like "upper case word ratio" or "exclamation mark count" as proxy indicators for emotional intensity

3. Beyond Basic Sentiment

   - Rather than just positive/negative, we could look at specific emotions (excitement, humor, awe, etc.)
   - The GoEmotions dataset (https://github.com/google-research/google-research/tree/master/goemotions) has models for detecting 27 different emotions in short text that might be applicable here

## 3.2 Model Selection and Training

Once we’ve engineered features like sentiment scores, topic clusters, and hashtag groupings, we can move into model training

### Recommended Approach

1. Start with Gradient Boosting

   - For this kind of problem, solutions with a gradient boosting model like XGBoost may be well-suited since:
     - They handle mixed feature types (categorical tags + numerical features)
     - Great with capturing non-linear relationships

2. Training Process

   - Something that happens quite often on TikTok is that a single video, which gains so much popularity, starts a trend. In training a model, training on earlier videos that rapidly become popular and then validating model performance on newer videos reflects what happens on TikTok on a daily basis
   - For the metrics, we should consider a combination of:
     - Recall: Since we care more about correctly identifying the viral videos than getting every prediction exactly right
     - RMSE (Root Mean Squared Error): To measure overall prediction accuracy for view counts, with higher penalties for larger prediction errors
     - MAE (Mean Absolute Error): For a more interpretable measure of prediction accuracy in actual view count units
