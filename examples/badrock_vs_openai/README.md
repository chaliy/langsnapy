# OpenAI vs. Bedrock Battle!

Runs a single set of questions against both OpenAI and Bedrock.

## Usage

Edit .env to add your API keys

```bash
pip install -r requirements.txt
cp .env.example .env
python main.py --participant bedrock
python main.py --participant openai

jupyter nbconvert --execute --to notebook --inplace results.ipynb 
jupyter notebook results.ipynb
```