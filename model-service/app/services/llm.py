from app.core.config import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=settings.OPENAI_TEMPERATURE,
        max_tokens=settings.OPENAI_MAX_TOKENS
    )

    return response.choices[0].message.content




# ChatCompletion(
# id='chatcmpl-BaF0QrAhPmLgJtbFXFO8F9nmMYEeI', 
# choices=[
#     Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='A string is a data type in programming that represents a sequence of characters.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))
# ], 
# created=1747977190, 
# model='gpt-3.5-turbo-0125', 
# object='chat.completion', 
# service_tier='default', 
# system_fingerprint=None, 
# usage=CompletionUsage(
#     completion_tokens=15, 
#     prompt_tokens=16, 
#     total_tokens=31, 
#     completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), 
#     prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
