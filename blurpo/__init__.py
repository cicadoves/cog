from pathlib import Path

from .bot import load_ext, load_url, prefix, run
from .func import load_env, EvalFile


__all__ = ['load_ext', 'load_url', 'prefix', 'run', 'load_env']

Path('exts/').mkdir(exist_ok=True)
Path('exts.eval').exists() or EvalFile('exts', init=True, val=set())
