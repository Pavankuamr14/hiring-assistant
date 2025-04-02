import google.generativeai as genai

genai.configure(api_key="api_key")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
