# app/services/ollama_client.py
import requests
import json
import time
from functools import lru_cache
from typing import Any, Dict, List, Union, Optional
from ..config import Config
from ..utils.prompt_templates import SYSTEM_PROMPT

OLLAMA_API = Config.OLLAMA_API
MODEL = Config.OLLAMA_MODEL

# Tunable defaults (lower max_tokens for snappier answers)
DEFAULT_MAX_TOKENS = 256
DEFAULT_TIMEOUT = 60
DEFAULT_TEMPERATURE = 0.0
DEFAULT_TOP_P = 0.9

# Reuse a single requests.Session to avoid connection overhead
_session: Optional[requests.Session] = None

def get_session() -> requests.Session:
    global _session
    if _session is None:
        s = requests.Session()
        # Optional: tune adapters (increase pool size)
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=50)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        _session = s
    return _session

def build_payload(user_prompt: str,
                  model: str = MODEL,
                  max_tokens: int = DEFAULT_MAX_TOKENS,
                  temperature: float = DEFAULT_TEMPERATURE,
                  top_p: float = DEFAULT_TOP_P,
                  stream: bool = True) -> Dict[str, Any]:
    # Keep system prompt compact; append minimal user instruction
    user_prompt_clean = user_prompt.strip()
    # Enforce JSON-only instruction only when user asks for test generation
    if any(k in user_prompt_clean.lower() for k in ("generate", "test case", "testcase", "write tests", "create tests", "return only json")):
        user_prompt_clean += "\n\nReturn ONLY a single valid JSON array. Do NOT include additional text."

    full_prompt = SYSTEM_PROMPT + "\n\nUSER PROMPT:\n" + user_prompt_clean

    payload = {
        "model": model,
        "prompt": full_prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": stream
    }
    return payload

def _parse_ndjson_line(line: str) -> Optional[Dict[str, Any]]:
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None

# Simple LRU cache for identical prompts (size limit adjustable)
@lru_cache(maxsize=128)
def _cached_response_for(prompt_key: str) -> Optional[Union[dict, list, str]]:
    # This wrapper exists to allow caching; actual call not cached here
    return None

def prewarm_model(sample_prompt: str = "Hello. Please respond briefly."):
    """
    Call once at service startup to warm the model and connection.
    """
    try:
        _ = generate_response(sample_prompt, max_tokens=16, timeout=15)
    except Exception:
        # ignore prewarm errors
        pass

def generate_response(user_prompt: str,
                      model: str = MODEL,
                      max_tokens: int = DEFAULT_MAX_TOKENS,
                      temperature: float = DEFAULT_TEMPERATURE,
                      top_p: float = DEFAULT_TOP_P,
                      timeout: int = DEFAULT_TIMEOUT) -> Union[dict, list, str]:
    """
    Stream NDJSON response from Ollama, stitch fragments together, try to parse JSON,
    fallback to text. Uses a persistent HTTP session and caches exact-prompt answers.
    """
    # quick cache check (exact-match prompts)
    cache_key = f"{model}|{temperature}|{top_p}|{max_tokens}||{user_prompt}"
    # attempt to read from lru_cache by calling the wrapper (store not implemented here)
    # Manual caching pattern: use dictionary or persistent cache if preferred. For simplicity:
    # We'll implement a tiny in-memory caching via function attribute
    cache_store = getattr(generate_response, "_cache_store", None)
    if cache_store is None:
        cache_store = {}
        setattr(generate_response, "_cache_store", cache_store)

    if cache_key in cache_store:
        return cache_store[cache_key]

    payload = build_payload(user_prompt, model=model, max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True)
    sess = get_session()

    start = time.time()
    resp = sess.post(OLLAMA_API, json=payload, stream=True, timeout=timeout)
    resp.raise_for_status()

    fragments: List[str] = []
    try:
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            parsed = _parse_ndjson_line(raw_line)
            if parsed and isinstance(parsed, dict):
                # common streamed fragment fields: "response", "text", "output"
                if "response" in parsed and isinstance(parsed["response"], str):
                    fragments.append(parsed["response"])
                elif "text" in parsed and isinstance(parsed["text"], str):
                    fragments.append(parsed["text"])
                elif "output" in parsed and isinstance(parsed["output"], str):
                    fragments.append(parsed["output"])
                # stop when signalled done
                if parsed.get("done") is True:
                    break
            else:
                # fallback: append raw line
                fragments.append(raw_line)
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ReadTimeout):
        # streaming issue — fallback to full body
        try:
            body_text = resp.text
            fragments = [body_text]
        except Exception:
            pass

    final_text = "".join(fragments).strip()

    # Attempt JSON parse
    result: Union[dict, list, str]
    try:
        parsed = json.loads(final_text)
        result = parsed
    except json.JSONDecodeError:
        # If the model emitted multiple JSON objects (rare), try to coerce:
        try:
            # try splitting by lines and parse each json object
            objs = []
            for line in final_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    objs.append(json.loads(line))
                except Exception:
                    # stop trying if parsing fails
                    objs = []
                    break
            if objs:
                result = objs
            else:
                result = final_text
        except Exception:
            result = final_text

    # store in small in-memory cache (expiration not implemented)
    try:
        cache_store[cache_key] = result
        # keep cache size bounded
        if len(cache_store) > 256:
            # drop oldest entry (not ordered, simple clear strategy)
            cache_store.clear()
    except Exception:
        pass

    elapsed = time.time() - start
    # optional: log elapsed time somewhere (print for now)
    # print(f"[ollama_client] generate_response elapsed {elapsed:.2f}s for prompt len {len(user_prompt)}")
    return result
